<?php
namespace app\admin\model;
use think\Model;
class Article extends Model
{

	public function cate(){
		return $this->belongsTo('cate','cateid');
	}



}
