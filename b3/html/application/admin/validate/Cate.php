<?php
namespace app\admin\validate;
use think\Validate;
class Cate extends Validate
{
    protected $rule = [
        'catename'  =>  'require|max:25|unique:cate',
    ];

    protected $message  =   [
        'catename.require' => '栏目名称必须填写',
        'catename.max' => '栏目名称长度不得大于25位',
        'catename.unique' => '栏目名称不得重复',

    ];

    protected $scene = [
        'add'  =>  ['catename'=>'require|unique:cate'],
        'edit'  =>  ['catename'=>'require|unique:cate'],
    ];




}
