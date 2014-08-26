#!/usr/local/bin/perl 

use DBI;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

# get db connection info from the environment
# use SetEnv in the Apache config for the cgi-bin directory to set these
$database  = $ENV{ALEPHRX_DATABASE_NAME};
$db_server = $ENV{ALEPHRX_DATABASE_HOST};
$user      = $ENV{ALEPHRX_DATABASE_USER};
$password  = $ENV{ALEPHRX_DATABASE_PASS};

$statement = "";
$value = "";
$count = 0;
$mailprog = $ENV{ALEPHRX_MAILER};
$from = "limstest\@itd.umd.edu (ALEPH Web Report)";
$id = "";

$input_size = $ENV { 'CONTENT_LENGTH' };
read ( STDIN, $form_info, $input_size );
@input_pairs = split (/[&;]/, $form_info);

%input = ();

foreach $pair (@input_pairs) {
  #Convert plusses to spaces
  $pair =~ s/\+/ /g;

  #Split the name and value pair
  ($name, $value) = split (/=/, $pair);

  #Decode the URL encoded name and value
  $name =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;
  $value =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;

  #Escape the single quotes
  $value =~ s/\'/\\\'/g;

  #Copy the name and value into the hash
  $input{$name} = $value;
}

$yes = $input{'yes'};
$no = $input{'no'};
$delete = $input{'delete'};
$filter_value = $input{'filter_value'};
$text = $input{'text'};
$id = $input{'record_id'}; 
$grp = $input{'grp'};
$campus = $input{'campus'};
$phone = $input{'phone'};
$name = $input{'name'};
$date = $input{'date'};
$status = $input{'status'};
$summary = $input{'summary'};
$rname = $input{'rname'};
$mresponse = $input{'response'};
$suppress = $input{'suppress'};
$mail = $input{'mail'};
$email = $input{'email'};
$cataloger = $input{'cataloger'};


$limit = $input{'limit'};
$CIRC = $input{'CIRC'};
$SRQ = $input{'SRQ'};
$DLM = $input{'DLM'};
$PAC = $input{'PAC'};
$CLOSED = $input{'CLOSED'};
$POST = $input{'POSTPONED'};
$NEW = $input{'NEW'};
$PEND = $input{'PENDING'};
$TECH = $input{'TECH'};
$RECORD = $input{'record'};
$NEXT = $input{'NEXT'};
$PREV = $input{'PREV'};
$LAST = $input{'LAST'};
$FIRST = $input{'FIRST'};
$p = $input{'page_increment'};
$sort_value = $input{'sort_value'};
$submit = $input{'submit'};
$drecord = $input{'drecord'};

#  Replaces escaped single quotes with single quotes in filter only.
$filter_value =~ s/\\'/\'/g;


if ($no) {
 
$message = "Delete aborted for record #$id<BR><BR>";

}

if ($yes) {

$message = "Record #$id has been deleted<BR><BR>";

&delete;

}


if ($submit){
    &insert;
#    $sort = $sort_value; unclear what this was doing
#}else{ 
}
$value = $ENV{'QUERY_STRING'};
$sort = $value;
#}



if ($delete) {

&pre_delete;

}else{ 


if ($filter eq "") {
    $filter = $filter_value;
}

&sort_value;
&filter;
&record;
&get_row_count;
&calc_num_pages;
&print_page_start;
&updated;
&next_paging;
&prev_paging;
&first_paging;
&last_paging;
&page_rules;
&first_last;
&get_sum_record;
&print_fetch;
#&display_records_paging;
&print_page_end;

&recipient;

if ($rname eq "") {
}else{
if ($mail eq "yes"){
    &response_date;
    &mail;
}
}

}



sub print_fetch {
print "<TABLE BORDER=0 CELLPADDING=2>\n";
print "<TR><TD></TD>\n";
print "<TD></TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"OLDFORM2.cgi?id\">ID</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B>Summary</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"OLDFORM2.cgi?grp\">Func. Area</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"OLDFORM2.cgi?people.name\">Name</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"OLDFORM2.cgi?campus\">Campus</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"OLDFORM2.cgi?status\">Status</TD>\n";
print "<TD BGCOLOR=\"#F3F49C\"><FONT SIZE=-1><B><a href=\"OLDFORM2.cgi?report.date\">Date</TD></TR>\n";
             print "</FORM>\n";
while (@row = $sth->fetchrow_array) {
             $response = "";
             &response_get;
             print "<TR><TD><FONT SIZE=+1 COLOR=\"#FF0000\">$response</FONT>\n</TD>";
             print "<FORM ACTION=\"\/cgi-bin\/ALEPH\/ALEPHurecord.cgi\" METHOD=\"post\">\n";
             print "<TD><FONT SIZE=-1><INPUT TYPE=\"submit\" VALUE=\"Update\"></TD>\n";
             print "<INPUT TYPE=\"hidden\" name=\"record\" VALUE=\"$row[0]\">\n";
             print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
             print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter\">\n";
             print "<INPUT TYPE=\"hidden\" name=\"sort_value\" VALUE=\"$sort\">\n";
             print "</FORM>\n";
             print "<TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1>#&nbsp;<a href=\"\/cgi-bin\/ALEPHsum_full.cgi?$row[0]\">$row[0]</TD>\n";
             print "<TD BGCOLOR=\"#BEE4BE\"><FONT SIZE=-1>&nbsp;$row[3]</TD>\n";
             print "<TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1>&nbsp;$row[1]</TD>\n";
             print "<TD BGCOLOR=\"#BEE4BE\"><FONT SIZE=-1>&nbsp;$row[7]</TD>\n";
             print "<TD BGCOLOR=\"#BEE4BE\"><FONT SIZE=-1>&nbsp;$row[2]</TD>\n";
             print "<TD BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1>&nbsp;$row[4]</TD>\n";
             print "<TD BGCOLOR=\"#BEE4BE\"><FONT SIZE=-1>&nbsp;$row[5]</TD>\n";
             print "<FORM ACTION=\"\/cgi-bin\/ALEPH\/OLDFORM2.cgi\" METHOD=\"post\">\n";
             print "<TD><FONT SIZE=-1><INPUT TYPE=\"submit\" VALUE=\"Delete\"></TD>\n";
             print "<INPUT TYPE=\"hidden\" name=\"delete\" VALUE=\"delete\">\n";
             print "<INPUT TYPE=\"hidden\" name=\"drecord\" VALUE=\"$row[0]\">\n";
             print "<INPUT TYPE=\"hidden\" name=\"record\" VALUE=\"$row[0]\">\n";
             print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
             print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter\">\n";
             print "<INPUT TYPE=\"hidden\" name=\"sort_value\" VALUE=\"$sort\">\n";
             print "</FORM>\n";
             $row_id = $row[0];
             $reply_count = "";
             $count = 0;
             &count_reply;
             print "<TD><FONT SIZE=+1 COLOR=\"#0000FF\">$reply_count</TD></TR>\n";

     }
}


#
#fetches all replies for printing
#

sub fetchreply {

$dbh_1 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_1 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text from reply where parent_id = '$row_id'";
$sth_1 = $dbh_1->prepare($statement_1)
    or die "Couldn't prepare the query: $sth_1->errstr";

$rv_1 = $sth_1->execute
    or die "Couldn't execute the query: $dbh_1->errstr";

          while (@rrow = $sth_1->fetchrow_array) {
    print "<TR>\n";
    print "<TD COLSPAN=2 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><i><FONT SIZE=-1 COLOR=\"3333CC\">&nbsp;Reply from:&nbsp;\n";
    print "$rrow[0]</TD>\n";
    print "<TD COLSPAN=4 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"3333CC\"><i>Date:&nbsp;$rrow[1]&nbsp;&nbsp;&nbsp;</TD>\n";
    print "<TD COLSPAN=1 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"3333CC\"><i>&nbsp;$rrow[2]</TD>\n";
    print "</TR>\n";
}
$rc_1 = $sth_1->finish;
$rc_1 = $dbh_1->disconnect;
}



#
#fetches reponse for printing
#


sub fetchresponse {


$dbh_2 = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_2 =   "SELECT name, DATE_FORMAT(date,'%m/%d/%y     %l:%i %p'), text from response where parent_id = '$row_id'";

$sth_2 = $dbh_2->prepare($statement_2)
    or die "Couldn't prepare the query: $sth_2->errstr";

$rv_2 = $sth_2->execute
    or die "Couldn't execute the query: $dbh_2->errstr";

          while (@row = $sth_2->fetchrow_array) {
              if ($row[0] eq "") {
      }else{
    print "<TR>\n";
    print "<TD COLSPAN=2 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><i><FONT SIZE=-1 COLOR=\"#A52A2A\">&nbsp;ITD Response from:&nbsp;\n";
    print "$row[0]</TD>\n";
    print "<TD COLSPAN=4 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"#A52A2A\"><i>Date:&nbsp;$row[1]&nbsp;&nbsp;&nbsp;</TD>\n";
    print "<TD COLSPAN=1 BGCOLOR=\"#BEE4BE\" VALIGN=TOP><FONT SIZE=-1 COLOR=\"#A52A2A\"><i>&nbsp;$row[2]</TD>\n";
    print "</TR>\n";
}
$rc_2 = $sth_2->finish;
$rc_2 = $dbh_2->disconnect;
}
}


#counts and creates flag to display when there is a reply


sub count_reply {


$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_7 =   "SELECT name from reply where parent_id = '$row_id'";
$sth_7 = $dbh->prepare($statement_7)
    or die "Couldn't prepare the query: $sth_7->errstr";

$rv_7 = $sth_7->execute
    or die "Couldn't execute the query: $dbh->errstr";


          while (@row = $sth_7->fetchrow_array) {
              $count++;
              $reply_count = '* ' x $count;
          }

$rc_7 = $sth_7->finish;
$rc_7 = $dbh->disconnect;
}


#creates flag to display when there is a response

sub count_response {


$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_8 =   "SELECT name from response where parent_id = '$row_id'";
$sth_8 = $dbh->prepare($statement_8)
    or die "Couldn't prepare the query: $sth_8->errstr";

$rv_8 = $sth_8->execute
    or die "Couldn't execute the query: $dbh->errstr";


          while (@rrow = $sth_8->fetchrow_array) {
              if ($rrow[0] eq ""){
              }else{
              $response_count = "*";
          }
          }

$rc_8 = $sth_8->finish;
$rc_8 = $dbh->disconnect;
}


sub response_get {

    if ($row[6] eq "") {
    }else{
        $response = "*";
    }
}


sub get_reply {

$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
$statement_9 =   "SELECT name from reply where parent_id = '$row_id'";
$sth_9 = $dbh->prepare($statement_9)
    or die "Couldn't prepare the query: $sth_9->errstr";

$rv_9 = $sth_9->execute
    or die "Couldn't execute the query: $dbh->errstr";

          while (@srow = $sth_1->fetchrow_array) {
              $count++;
              $reply_count = '* ' x $count;
}
$rc_9 = $sth_9->finish;
$rc_9 = $dbh->disconnect;
}

#
#queries the database to get the total number of records, used to calculate the
#total number of pages 
#
sub get_row_count {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement_10 =   "SELECT COUNT(*) from report, people where report.id = people.id $filter";
    $sth_10 = $dbh->prepare($statement_10)
    or die "Couldn't prepare the query: $sth_10->errstr";

    $rv_10 = $sth_10->execute
    or die "Couldn't execute the query: $dbh->errstr";

    while (@crow = $sth_10->fetchrow_array) {
        $row_count = $crow[0];
    }
    $rc_10 = $sth_10->finish;
    $rc_10 = $dbh->disconnect;
}

#
#calculates the total number pages that will be used for all the database
#
sub calc_num_pages {

    $num_pages_1 = $row_count / 30;
    $num_pages_2 = sprintf("%d\n", $num_pages_1);
    if ($num_pages_1 > $num_pages_2){
        $num_pages = $num_pages_2 + 1;
    }else{
    $num_pages = $num_pages_2;
    } 
}

#
#increments the page variable, prints the hidden increment value to pass on to the next page
#
sub next_paging {

    if ($NEXT) {
              $p++;
              print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
              }
}

#
#
sub last_paging {

    if ($LAST) {
              $p = $num_pages - 1;
              print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
}
}


#
#
sub first_paging {

    if ($FIRST) {
              $p = 0;
              print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
}
}



#
#decrements the page variable, prints the hidden increment value to pass on to the next page
#
sub prev_paging {

    if ($PREV) {
               $p--;
               print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";

}
}


#
#page_rules decides how the next and previous buttons will display.
#
sub page_rules {
     if ($p < 1){
     }else{
     print "<FONT SIZE=-1><INPUT TYPE=\"submit\" VALUE=\"<< FIRST PAGE\" NAME=\"FIRST\">\n";
     print "<INPUT TYPE=\"submit\"  VALUE=\"< PREVIOUS PAGE\" NAME=\"PREV\"></FONT>\n";

 }
     if ($p > $num_pages-2) {
     }else{
         if ($value =~ /\d/){
    end;
}elsif($LAST) {
  }else{

     print "<FONT SIZE=-1><INPUT TYPE=\"submit\" VALUE=\"NEXT PAGE >\" NAME=\"NEXT\">\n";
     print "<INPUT TYPE=\"submit\" VALUE=\"LAST PAGE >>\" NAME=\"LAST\"></FONT>\n";
 }
 }
$limit = $p * 30; 
     print "<BR>\n";
 }



sub first_last {

if ($LAST) {
    $limit = ($num_pages - 1) * 30;
}
if ($FIRST) {
    $limit = 0;
}
}



#sets the filter varible 


sub filter {

if ($CIRC) {
    $filter = "and people.grp = 'CIRC'";
}

if ($PAC) {
    $filter = "and people.grp = 'PAC'";
}

if ($SRQ) {
    $filter = "and people.grp = 'SRQ'";
}

if ($DLM) {
    $filter = "and people.grp = 'DLM'";
}

if ($CLOSED) {
    $filter = "and report.status = 'closed'";
}

if ($PEND) {
    $filter = "and report.status = 'pending'";
}

if ($POST) {
    $filter = "and report.status = 'postpone'";
}

if ($NEW) {
    $filter = "and report.status = 'new'";
}

if ($TECH) {
    $filter = "and people.grp = 'TECH'";
}

#    $filter_value = $filter;
}



#prints the page start and hidden variables 

sub print_page_start {

print "Content-type: text/html\n\n";
print "<HTML>\n<HEAD><BR>\n";
print "<TITLE>Aleph Reports Maintenance</TITLE>\n</HEAD>\n<BODY BACKGROUND=\"\/IMG\/bk2.gif\">\n";
print "<FORM ACTION=\"OLDFORM2.cgi?id\" METHOD=\"post\">\n";
print "<a NAME=\"top\"></a>\n";
print "<center>\n";
print "<H1>ALEPH Reports Maintenance</H1>\n";
#print "<P>Filter by:&nbsp;<INPUT TYPE=\"submit\" VALUE=\"CIRC\" NAME=\"CIRC\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"SRQ\" NAME=\"SRQ\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"PAC\" NAME=\"PAC\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"DLM\" NAME=\"DLM\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"TECH\" NAME=\"TECH\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"New\" NAME=\"NEW\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"Pending\" NAME=\"PENDING\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"Postponed\" NAME=\"POSTPONED\">\n";
#print "<INPUT TYPE=\"submit\" VALUE=\"Closed\" NAME=\"CLOSED\">\n";
#print "<INPUT TYPE=\"button\" VALUE=\"All Summaries\" onClick=\"parent.location='OLDFORM2.cgi?id'\"></p>\n";
print "<P><FONT SIZE=+1 COLOR=\"#FF0000\">&nbsp;&nbsp;*</FONT><FONT SIZE=-1>&nbsp;&nbsp;Indicates an ITD response.&nbsp;</FONT>\n";
print "<INPUT TYPE=\"button\" VALUE=\"Report Web Form\" onClick=\"parent.location ='\/cgi-bin\/ALEPHform.cgi'\">\n";
print "<INPUT TYPE=\"button\" VALUE=\"Report Statistics\" onClick=\"parent.location ='\/cgi-bin\/ALEPHstats.cgi'\">\n";
#print "<INPUT TYPE=\"button\" VALUE=\"ALEPH Reports\" onClick=\"parent.location='ALEPHsort.cgi?id'\">\n";
print "<FONT SIZE=+1 COLOR=\"#0000FF\">&nbsp;&nbsp;*</FONT><FONT SIZE=-1>&nbsp;&nbsp;Indicates a User reply.</FONT></p>\n";
print "</FORM>\n";
print "<FORM ACTION=\"\/cgi-bin\/ALEPH\/ALEPHurecord.cgi\" METHOD=\"post\">\n";
print "<B>Go to report # :</B>\n";
print "<INPUT TYPE=\"text\" NAME=\"record\" SIZE=3>\n";
print "<INPUT TYPE=\"submit\" VALUE=\"GO\">&nbsp;&nbsp;\n";
print "<INPUT TYPE=\"button\" VALUE=\"Search\" onClick=\"parent.location='ALEPHsearch.cgi'\"></p>\n";
print "</FORM>\n";

print "<FORM ACTION=\"OLDFORM2.cgi?id\" METHOD=\"post\">\n";
print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter\">\n";
print "<INPUT TYPE=\"hidden\" name=\"sort_value\" VALUE=\"$sort\">\n";
print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
print "<FONT COLOR=\"#FF0000\">$message</FONT>\n";

}

#prints the page end

sub print_page_end {

print "</TABLE>\n";
$rc = $sth->finish;
$rc = $dbh->disconnect;
print "<BR>\n";
#&page_rules;
print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter\">\n";
print "</FORM>\n";
print "<CENTER><a href=\"#top\"><FONT SIZE=-1>TOP</a>\n";
print "<BR><BR>\n";
print "</BODY>\n</HTML>\n";

} 




sub fetchrow {
while (@row = $sth->fetchrow_array) {
print 
        print "<TR><TD BGCOLOR=\"#F3F49C\" COLSPAN=7><B><i>Report #</i>&nbsp;$row[0]&nbsp;&nbsp;&nbsp;&nbsp;$row[1]</B></TD></FONT></TR>\n";

         print "<TR>\n
         <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Name</I></TH>\n
         <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Phone</I></TH>\n
         <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Date</I></TH>\n
         <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Func. Area</I></TH>\n
         <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Campus</I></TH>\n
         <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Status</I></TH>\n
         <TH BGCOLOR=\"#FFFFCC\"><FONT SIZE=-1 COLOR=\"cc9933\"><I>Text</I></TH>\n";

        print "<TR>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[2]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[3]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[4]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[5]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[6]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[7]</TD>\n";
        print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[8]</TD>\n";
        print "<TD VALIGN=TOP>$row[9]<FONT SIZE=-2><a href=\"ALEPHreply.cgi?$row[0]\">Reply</a></FONT></TD>\n";
        $row_id = $row[0];
        &fetchresponse(); # fetch the response
        print "</TR>\n";
        &fetchreply();    # fetch the replies
        print "</TR>\n";
        print "<TR><TD><FONT SIZE=-2>&nbsp;</TD></TR>\n";
        print "<TR><TD>$reply_count</TD></TR>\n";
    }
}


sub record {

if ($RECORD){
    if ($RECORD eq ""){
        $RECORD = "id";
    }
}

if ($RECORD) {
    if ($RECORD =~ /\D/) {
    $value = "id";
}else{
    $value = $RECORD;

}
}
}





sub get_sum_record {

$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

$statement =   "SELECT people.id, people.grp, people.campus, report.summary, report.status, DATE_FORMAT(report.date,'%m/%d/%y'), response.name, people.name FROM people, report, response WHERE report.supress = 'no' and people.id = report.id and people.id = response.parent_id $filter ORDER BY $sort LIMIT $limit, 30";


#need to replace "order by $sort" to the above query 


$sth = $dbh->prepare($statement)
         or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
         or die "Couldn't execute the query: $dbh->errstr";

}


#inserts the data when updating a record


sub insert {

    if ($grp) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE people SET people.grp = '$grp' WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($status) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE report SET report.status = '$status' WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($text) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE report SET report.text = '$text' WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($summary) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE report SET report.summary = '$summary' WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($campus) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE people SET people.campus = '$campus' WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($date) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE report SET report.date = '$date' WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($name) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE people SET people.name = '$name' WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($phone) {
        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE people SET people.phone = '$phone' WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($rname) {

        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE response SET response.name ='$rname', response.text = '$mresponse', response.date = NOW() where parent_id = $id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($suppress) {

        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE report SET report.supress ='$suppress' where report.id = $id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

    if ($email) {

         $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
         $statement =   "UPDATE people SET people.email ='$email' where people.id = $id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }


    if ($cataloger) {

        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
        $statement =   "UPDATE report SET report.cataloger ='$cataloger' where report.id = $id";

$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

    }

}




sub mail {

$text =~ s/\\'/\'/g;
$mresponse =~ s/\\'/\'/g;
$summary =~ s/\\'/\'/g;



    if ($mail eq "yes") {
        open (MAIL,"|$mailprog -t");
        print MAIL "To:$recipient\n";
        print MAIL "Cc:support\@itd.umd.edu\n";
        print MAIL "From: $from\n";
        print MAIL "Subject: RE:#$id:$summary\n";
        print MAIL "This is a RESPONSE to the ALEPH Web Report listed below\n";
        print MAIL "http:\/\/www.itd.umd.edu\/cgi-bin\/ALEPHsum_full.cgi?$id\n";
        print MAIL "\n";
        print MAIL "\n";
        print MAIL "Response Submitted by: $rname\n";
        print MAIL "     Date of Response: $rdate\n";
        print MAIL "      Functional Area: $grp\n";
        print MAIL "   Original Report # : $id\n";
        print MAIL "\n";
        print MAIL "Response: $mresponse\n";
        print MAIL "\n";
        print MAIL "<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>\n";
        print MAIL "\n";
        print MAIL "             Report #: $id\n";
        print MAIL "                 Date: $date\n";
        print MAIL "         Submitted by: $name\n";
        print MAIL "\n";
        print MAIL "\n";
        print MAIL "Report: $text\n";
        print MAIL "\n";
        close (MAIL);
        $row_id = "";
    } else {
        end;}
}

#sets the recipient variable according to the "grp" value of the report record.

sub recipient {

    if ($grp eq "Circulation") {
        $recipient = "3circ\@itd.umd.edu";
    }
    if ($grp eq "Reserves") {
        $recipient = "3circ\@itd.umd.edu";
    }
    if ($grp eq "Web OPAC") {
        $recipient = "3pac\@itd.umd.edu";
    }

    if ($grp eq "Cataloging") {
        $recipient = "3dlm\@itd.umd.edu";
    }

    if ($grp eq "Serials") {
        $recipient = "3srq\@itd.umd.edu";
    }

    if ($grp eq "other") {
        $recipient = "3itd\@itd.umd.edu";
    }
    if ($grp eq "Acquisitions") {
        $recipient = "3srq\@itd.umd.edu";
    }
    if ($grp eq "Technical") {
        $recipient = "3tech\@itd.umd.edu";
    }
    if ($grp eq "Item Maintenance") {
        $recipient = "3dlm\@itd.umd.edu";
    }

}


sub response_date {

    $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);
    $statement =   "SELECT date from response where parent_id = $id";

$sth_6 = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth_6->errstr";
$rv_6 = $sth_6->execute
    or die "Couldn't execute the query: $dbh->errstr";

    while (@row = $sth_6->fetchrow_array) {
        $rdate = $row[0];
    }
    $rc_6 = $sth_6->finish;
$rc_2 = $dbh->disconnect
}


sub display_records_paging {

    $sort = $value;

    if ($NEXT) {
        $sort = $sort_value;
    }
    if ($PREV) {
        $sort = $sort_value;
    }
    if ($LAST) {
        $sort = $sort_value;
    }
    if ($FIRST) {
        $sort = $sort_value;
    }
}



sub updated {

    if ($submit){
    print "<P><FONT COLOR=\"#FF0000\"> Record $id has been updated!</FONT></P>\n";
}
}





sub sort_value {

     
     if ($NEXT) {
         $sort = $sort_value;
     }
     if ($PREV) {
         $sort = $sort_value;
     }
     if ($LAST) {
         $sort = $sort_value;
     }
     if ($FIRST) {
         $sort = $sort_value;
     }
     
     if ($sort_value eq ""){
         $sort_value = "id";
     }
     
     if ($value eq ""){
         $sort = $sort_value;
     }

}



# deletes the selected records from the database
 
sub delete {

        $dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);

        $statement =   "DELETE from people WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";


        $statement =   "DELETE from report WHERE id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";

        $statement =   "DELETE from response WHERE parent_id = $id";
$sth = $dbh->prepare($statement)
    or die "Couldn't prepare the query: $sth->errstr";
$rv = $sth->execute
    or die "Couldn't execute the query: $dbh->errstr";


}


#presents the selected record for deletetion, offers the yes or no option.  If no is 
#selected user is taken back to summary screen 

sub pre_delete  {


$dbh = DBI->connect("DBI:mysql:$database:$db_server", $user, $password);


$statement =   "SELECT people.id, people.grp, people.campus, people.phone, people.name, report.date, report.status, report.summary, report.text FROM people, report WHERE people.id = report.id AND people.id = $drecord";

$sth = $dbh->prepare($statement)
         or die "Couldn't prepare the query: $sth->errstr";

$rv = $sth->execute
         or die "Couldn't execute the query: $dbh->errstr";



print "Content-type: text/html\n\n";
print "<HTML>\n<HEAD>\n<TITLE>ALEPH Record Maintenance</TITLE>\n</HEAD>\n<BODY BACKGROUND=\"\/IMG\/bk2.gif\">\n";
print "<FORM ACTION=\"OLDFORM2.cgi\" METHOD=\"post\">\n";
print "<INPUT TYPE=\"hidden\" NAME=\"record_id\" VALUE=\"$drecord\">\n";
print "<center>\n";
print "<P><h1>ALEPH Records Maintenance</P></h1>\n";
print "<FONT COLOR=\"#FF0000\">You are about to delete the following record!</FONT>\n";
print "<P><INPUT TYPE=\"submit\" VALUE=\"YES\" NAME=\"yes\">\n"; 
print "&nbsp;&nbsp;<INPUT TYPE=\"submit\" VALUE=\"NO\" NAME=\"no\"</P>\n";
print "<INPUT TYPE=\"hidden\" name=\"record\" VALUE=\"$row[0]\">\n";
print "<INPUT TYPE=\"hidden\" name=\"page_increment\" VALUE=\"$p\">\n";
print "<INPUT TYPE=\"hidden\" name=\"filter_value\" VALUE=\"$filter_value\">\n";
print "<INPUT TYPE=\"hidden\" name=\"sort_value\" VALUE=\"$sort\">\n";
print "<BR>\n";
print "<BR>\n";
print "<TABLE BORDER=0 BGCOLOR=\"FFFCC\">\n";
print "<TR>\n
          <TH>ID</TH>\n
          <TH ALIGN=LEFT>funct.area</TH>\n
          <TH ALIGN=LEFT>campus</TH>\n
          <TH ALIGN=LEFT>phone</TH>\n
          <TH ALIGN=LEFT>name</TH>\n
          <TH ALIGN=LEFT>date</TH>\n
          <TH ALIGN=LEFT>status</TH>\n
          <TH ALIGN=LEFT>summary</TH>\n
          <TH ALIGN=LEFT>text</TH>\n";

while (@row = $sth->fetchrow_array) {
          print "<TR>\n";
          print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[0]</TD>\n";
          print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[1]</TD>\n";
          print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[2]</TD>\n";
          print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[3]</TD>\n";
          print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[4]</TD>\n";
          print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[5]</TD>\n";
          print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[6]</TD>\n";
          print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[7]</TD>\n";
          print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[8]</TD>\n";
          print "<TD BGCOLOR=\"#BEE4BE\" VALIGN=TOP>$row[9]</TD>\n";
          print "</TR>\n";
      }

$rc = $sth->finish;
$rc = $dbh->disconnect;
print "</TABLE>\n";
print "</FORM>\n";
print "<BR>\n";
print "</BODY>\n</HTML>\n";


}













