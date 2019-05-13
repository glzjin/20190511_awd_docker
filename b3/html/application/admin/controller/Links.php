<?php
namespace app\Admin\controller;
use app\admin\model\Links as LinksModel;
use app\admin\controller\Base;
class Links extends Base
{
    public function lst()
    {
    	$list = LinksModel::paginate(3);
    	$this->assign('list',$list);
        return $this->fetch();
    }

    public function add()
    {	
    	if(request()->isPost()){

			$data=[
    			'title'=>input('title'),
                'url'=>input('url'),
    			'desc'=>input('desc'),
    		];
    		$validate = \think\Loader::validate('Links');
    		if(!$validate->scene('add')->check($data)){
			   $this->error($validate->getError()); die;
			}
    		if(db('Links')->insert($data)){
    			return $this->success('添加链接成功！','lst');
    		}else{
    			return $this->error('添加链接失败！');
    		}
    		return;
    	}
        return $this->fetch();
    }

    public function edit(){
    	$id=input('id');
    	$Links=db('Links')->find($id);
    	if(request()->isPost()){
    		$data=[
    			'id'=>input('id'),
                'title'=>input('title'),
                'url'=>input('url'),
    			'desc'=>input('desc'),
    		];
			$validate = \think\Loader::validate('Links');
    		if(!$validate->scene('edit')->check($data)){
			   $this->error($validate->getError()); die;
			}
    		if(db('Links')->update($data)){
    			$this->success('修改链接成功！','lst');
    		}else{
    			$this->error('修改链接失败！');
    		}
    		return;
    	}
    	$this->assign('Links',$Links);
    	return $this->fetch();
    }

    public function del(){
    	$id=input('id');
		if(db('Links')->delete(input('id'))){
			$this->success('删除链接成功！','lst');
		}else{
			$this->error('删除链接失败！');
		}
    	
    }



}
