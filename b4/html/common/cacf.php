<?php
class chybeta{
	//
	var $test = 'pcaq';
	function __wakeup(){
		$fp = fopen("log.php","w") ;
		fwrite($fp,$this->test);
		fclose($fp);
	}
}
//判断是否是序列化
function is_serialized( $data ) {
     $data = trim( $data );
     if ( 'N;' == $data )
         return true;
     if ( !preg_match( '/^([adObis]):/', $data, $badions ) )
         return false;
     switch ( $badions[1] ) {
         case 'a' :
         case 'O' :
         case 's' :
             if ( preg_match( "/^{$badions[1]}:[0-9]+:.*[;}]\$/s", $data ) )
                 return true;
             break;
         case 'b' :
         case 'i' :
         case 'd' :
             if ( preg_match( "/^{$badions[1]}:[0-9.E-]+;\$/", $data ) )
                 return true;
             break;
     }
     return false;
 }


if(isset($_POST['name'])){
	$post_data=$_POST['name'];
	if(is_serialized($post_data)){
	echo $post_data;
	unserialize($post_data);
}
else{
	echo "Hello ".$post_data.",Your resume scored ".mt_rand(60,100)." points";
}

}
else{
	echo("请输入你的名字");
}

// $class4 = new chybeta();
// $class4->test = '';	
// $class4_ser = serialize($class4);
// print_r($class4_ser);
?>
<html>
<form action="#" method="post">
<input type="text" name="name">
<input type="submit" name="submit" value="提交">
</form>
</html>