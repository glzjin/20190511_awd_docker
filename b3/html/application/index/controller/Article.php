<?php
namespace app\index\controller;
use app\index\controller\Base;
class Article extends Base
{

    public function index()
    {
    	$arid=input('arid');
    	$articles=db('article')->find($arid);
        $ralateres=$this->ralat($articles['keywords'],$articles['id']);
        // dump($ralateres); die;
    	db('article')->where('id','=',$arid)->setInc('click');
    	$cates=db('cate')->find($articles['cateid']);
    	$recres=db('article')->where(array('cateid'=>$cates['id'],'state'=>1))->limit(8)->select();
    	$this->assign(array(
    		'articles'=>$articles,
    		'cates'=>$cates,
    		'recres'=>$recres,
            'ralateres'=>$ralateres
    		));
        return $this->fetch('article');
    }


    public function ralat($keywords,$id){
        $arr=explode(',', $keywords);
        static $ralateres=array();
        foreach ($arr as $k=>$v) {
            $map['keywords']=['like','%'.$v.'%'];
            $map['id']=['neq',$id];
            $artres=db('article')->where($map)->order('id desc')->limit(8)->select();
            $ralateres=array_merge($ralateres,$artres);
        }
        if($ralateres){

        $ralateres=arr_unique($ralateres);

        return $ralateres;
            
        }
        
    }



    




}
