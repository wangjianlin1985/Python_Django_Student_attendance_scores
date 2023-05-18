$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/AttendanceState/update/" + $("#attendanceState_stateId_modify").val(),
		type : "get",
		data : {
			//stateId : $("#attendanceState_stateId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (attendanceState, response, status) {
			$.messager.progress("close");
			if (attendanceState) { 
				$("#attendanceState_stateId_modify").val(attendanceState.stateId);
				$("#attendanceState_stateId_modify").validatebox({
					required : true,
					missingMessage : "请输入状态编号",
					editable: false
				});
				$("#attendanceState_stateName_modify").val(attendanceState.stateName);
				$("#attendanceState_stateName_modify").validatebox({
					required : true,
					missingMessage : "请输入状态名称",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#attendanceStateModifyButton").click(function(){ 
		if ($("#attendanceStateModifyForm").form("validate")) {
			$("#attendanceStateModifyForm").form({
			    url:"AttendanceState/update/" + $("#attendanceState_stateId_modify").val(),
			    onSubmit: function(){
					if($("#attendanceStateEditForm").form("validate"))  {
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
			$("#attendanceStateModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
