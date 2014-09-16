#!/usr/bin/perl -w
use strict;

use FindBin qw{$Bin};
use lib "$Bin/../lib";

use CGI;
use URI;
use XML::Simple;

use AlephRx::Database;

my $q = CGI->new;

# must be a POST request
if ($q->request_method ne 'POST') {
    print $q->header(-type => 'text/plain', -status => 405, -allow => 'POST');
    print "Only POST requests are allowed to this URL.\n";
    exit;
}
# must be an XML content type
if ($q->content_type !~ m{^(application|text)/xml\b}) {
    print $q->header('text/plain', 415);
    printf "Expecting XML data (text/xml or application/xml); got '%s'\n",
        $q->content_type;
    exit;
}

# do an XML::Simple parse of the POST body data, with empty elements represented
# as the empty string (so the resulting data structure will be similar to form
# submission of an empty field)
my $data = eval {
    XMLin($q->param('POSTDATA'), SuppressEmpty => '');
};
if ($@) {
    print $q->header('text/plain', 400);
    print "Unable to parse submitted data as XML.\n";
    exit;
}

# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
my $database  = $ENV{ALEPHRX_DATABASE_NAME};
my $db_server = $ENV{ALEPHRX_DATABASE_HOST};
my $user      = $ENV{ALEPHRX_DATABASE_USER};
my $password  = $ENV{ALEPHRX_DATABASE_PASS};

my $db = AlephRx::Database->new(
    "DBI:mysql:$database:$db_server",
    $user,
    $password
);

# check the submitted data for errors
my @errors = $db->validate_data($data);
if (@errors) {
    print $q->header('text/plain', 400);
    print "Missing or invalid fields.\n\n";
    print join "\n", @errors;
} else {
    # create the report in the database
    my $report = $db->submit_report($data);
    if ($report) {
        # if successful, respond with the URL for the report details page of the
        # newly created report
        print $q->header('text/plain');
        my $url = URI->new_abs('ALEPH16/ALEPHsum_full.cgi', $q->url);
        $url->query($report->id);
        print "$url\n";
    } else {
        print $q->header('text/plain', 500);
        print "Unable to create record.\n";
    }
}
