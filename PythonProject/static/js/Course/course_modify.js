$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Course/update/" + $("#course_courseNo_modify").val(),
		type : "get",
		data : {
			//courseNo : $("#course_courseNo_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (course, response, status) {
			$.messager.progress("close");
			if (course) { 
				$("#course_courseNo_modify").val(course.courseNo);
				$("#course_courseNo_modify").validatebox({
					required : true,
					missingMessage : "请输入课程编号",
					editable: false
				});
				$("#course_courseName_modify").val(course.courseName);
				$("#course_courseName_modify").validatebox({
					required : true,
					missingMessage : "请输入课程名称",
				});
				$("#course_teacherName_modify").val(course.teacherName);
				$("#course_courseCount_modify").val(course.courseCount);
				$("#course_courseCount_modify").validatebox({
					required : true,
					validType : "integer",
					missingMessage : "请输入总课时",
					invalidMessage : "总课时输入不对",
				});
				$("#course_courseScore_modify").val(course.courseScore);
				$("#course_courseScore_modify").validatebox({
					required : true,
					validType : "number",
					missingMessage : "请输入总学分",
					invalidMessage : "总学分输入不对",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#courseModifyButton").click(function(){ 
		if ($("#courseModifyForm").form("validate")) {
			$("#courseModifyForm").form({
			    url:"Course/update/" + $("#course_courseNo_modify").val(),
			    onSubmit: function(){
					if($("#courseEditForm").form("validate"))  {
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
                	var obj = jQuery.parseJSON(data);
                    if(obj.success){
                        $.messager.alert("消息","信息修改成功！");
                        $(".messager-window").css("z-index",10000);
                        //location.href="frontlist";
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    } 
			    }
			});
			//提交表单
			$("#courseModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
