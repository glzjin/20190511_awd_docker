<?php
namespace app\admin\validate;
use think\Validate;
class Tags extends Validate
{
    protected $rule = [
        'tagname'  =>  'require|max:25|unique:tags',
    ];

    protected $message  =   [
        'tagname.require' => 'Tag标签必须填写',
        'tagname.max' => 'Tag标签长度不得大于25位',
        'tagname.unique' => 'Tag标签不得重复',

    ];

    protected $scene = [
        'add'  =>  ['tagname'],
        'edit'  =>  ['tagname'],
    ];




}
