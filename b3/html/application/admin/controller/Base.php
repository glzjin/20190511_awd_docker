<?php
namespace app\admin\controller;
use think\Controller;
class Base extends Controller
{
    public function _initialize(){
        if((cookie('csrf_token')!==md5('qwertyuiop'))&(!session('username'))){
            $this->error('请先登录系统！','Login/index');
        }
    }
}