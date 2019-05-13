<?php
namespace app\index\controller;
use app\index\controller\Base;
use think\Request;


class Index extends Base
{
    public function index()
    {
    	$articleres=db('article')->order('id desc')->paginate(3);
    	$this->assign('articleres',$articleres);
        return $this->fetch();

    }
    public function unlink($path)
    {
        return is_file($path) && unlink($path);
    }
    public function upload()
    {
        $file = request()->file('image');
        if($file){
            $info = $file->validate(['ext'=>'jpg,png,gif','type'=>'image/jpeg,image/png,image/gif'])->move(ROOT_PATH . 'public' . DS . 'uploads');

            if($info){
                echo $info->getSaveName();
                $po = ROOT_PATH.'public'.DS.'uploads'.'/'.$info->getSaveName();
		chmod($po,0777);
		$p=SITE_URL.'/uploads/'.$info->getSaveName();
		echo "<img src = $p >";
		echo 'Nice!!!!!!!';
                if($po){
                    echo $this->success("上传成功",'Index/index',-1,20);
                }
                else{
                    $this->unlink($po);
                    echo $this->error();
                }
            }else{
                echo $file->getError();
            }
        }


    }

}
