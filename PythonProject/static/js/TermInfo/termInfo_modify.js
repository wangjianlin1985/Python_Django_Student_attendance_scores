$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/TermInfo/update/" + $("#termInfo_termId_modify").val(),
		type : "get",
		data : {
			//termId : $("#termInfo_termId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (termInfo, response, status) {
			$.messager.progress("close");
			if (termInfo) { 
				$("#termInfo_termId_modify").val(termInfo.termId);
				$("#termInfo_termId_modify").validatebox({
					required : true,
					missingMessage : "请输入学期编号",
					editable: false
				});
				$("#termInfo_termName_modify").val(termInfo.termName);
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#termInfoModifyButton").click(function(){ 
		if ($("#termInfoModifyForm").form("validate")) {
			$("#termInfoModifyForm").form({
			    url:"TermInfo/update/" + $("#termInfo_termId_modify").val(),
			    onSubmit: function(){
					if($("#termInfoEditForm").form("validate"))  {
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
			$("#termInfoModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
