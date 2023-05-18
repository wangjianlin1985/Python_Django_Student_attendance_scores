$(function () {
	$("#course_courseNo").validatebox({
		required : true, 
		missingMessage : '请输入课程编号',
	});

	$("#course_courseName").validatebox({
		required : true, 
		missingMessage : '请输入课程名称',
	});

	$("#course_courseCount").validatebox({
		required : true,
		validType : "integer",
		missingMessage : '请输入总课时',
		invalidMessage : '总课时输入不对',
	});

	$("#course_courseScore").validatebox({
		required : true,
		validType : "number",
		missingMessage : '请输入总学分',
		invalidMessage : '总学分输入不对',
	});

	//单击添加按钮
	$("#courseAddButton").click(function () {
		//验证表单 
		if(!$("#courseAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#courseAddForm").form({
			    url:"/Course/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#courseAddForm").form("validate"))  { 
	                	$.messager.progress({
							text : "正在提交数据中...",
						}); 
	                	return true;
	                } else {
	                    return false;
	                }
			    },
			    success:function(data){
			    	$.messager.progress("close");
                    //此处data={"Success":true}是字符串
                	var obj = jQuery.parseJSON(data); 
                    if(obj.success){ 
                        $.messager.alert("消息","保存成功！");
                        $(".messager-window").css("z-index",10000);
                        $("#courseAddForm").form("clear");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#courseAddForm").submit();
		}
	});

	//单击清空按钮
	$("#courseClearButton").click(function () { 
		//$("#courseAddForm").form("clear"); 
		location.reload()
	});
});
