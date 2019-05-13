<?php
namespace app\index\controller;
use app\index\controller\Base;
class Cate extends Base
{
    public function index()
    {
    	$cateid=input('cateid');
    	//查询当前栏目名称
    	$cates=db('cate')->find($cateid);
    	$this->assign('cates',$cates);
    	//查询当前栏目下的文章
    	$articleres=db('article')->where(array('cateid'=>$cateid))->paginate(3);
    	$this->assign('articleres',$articleres);
        return $this->fetch('cate');
    }




}