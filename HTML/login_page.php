<?php
$HOST = '127.0.0.1';
$USER = 'user280';
$PASS = 'p4ssw0rd';
$DB = 'project280';
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$pdo = new PDO("mysql:host=$HOST;port=3306;dbname=$DB", $USER, $PASS);
$show_error=isset($_COOKIE['ShowError']);
$show_success=isset($_COOKIE['ShowSuccess']);
setcookie("ShowError", "", time()-3600);
setcookie("ShowSuccess", "", time()-3600);
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>EugeneNeedsLove.com</title>
    <link rel="stylesheet" href="resources/style.css" />
  </head>
  <body>
    <h1 class="title">
      <img src="resources/logo.png" alt="EugeneNeedsLove.com">
    </h1>
<?php
		if ($show_success) {
			echo "<p>You're on this list!</p>";
		}
		else {
			if ($show_error) {
				echo "<p>Please correct error(s) and try again</p>";
			}
?>
   <section>
	<form action="insert.php" method="POST">
	  <h2>Join the Club!</h2>
	  <p>
        <label for="FirstName">First Name:</label> <input type="text" name="firstname" id="FirstName" />
      </p>
      <p>
        <label for="LastName">Last Name:</label> <input type="text" name="lastname" id="LastName" />
      </p>
      <p>
        <label for="Phone">Phone Number:</label> <input type="text" name="phone" id="Phone" />
      </p>
      <p>
        <label for="Age">Age:</label> <input type="number" name="age" id="Age" min="18" max="99" value="" />
      </p>
      <p>
        I'm interested in&hellip;
      </p>
      <p>
<?php
		$q = "SELECT id, name FROM Interests ORDER BY sort_order";
		$result = $pdo->query($q);
		while ($row = $result->fetch()) {
		    printf('<input type="checkbox" name="interests" id="Int%s" value="%s"><label for="Int%s">%s</label> ', $row[0], $row[0], $row[0], htmlspecialchars($row[1]));
		}
?>
      <p>
        <input type="submit" value="Get in line!" />
      </p>
<?php
		}
?>
    </form>
</section>

    <section id="TheLine">
	    <h2>The line:</h2>
	    <ol>
<?php
			$q = "SELECT first_name, last_name FROM People ORDER BY time_added";
			$result = $pdo->query($q);
			while ($row = $result->fetch()) {
			    printf('<li>%s %s</li>', htmlspecialchars($row['first_name']), htmlspecialchars($row['last_name']));
			}
?>
	   	</ol>
   </section>
    <img src="resources/looking_forward.jpg" id="BottomImage" />
  </body>
</html>