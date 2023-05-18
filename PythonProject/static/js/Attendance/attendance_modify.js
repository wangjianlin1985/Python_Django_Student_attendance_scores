$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Attendance/update/" + $("#attendance_attendanceId_modify").val(),
		type : "get",
		data : {
			//attendanceId : $("#attendance_attendanceId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (attendance, response, status) {
			$.messager.progress("close");
			if (attendance) { 
				$("#attendance_attendanceId_modify").val(attendance.attendanceId);
				$("#attendance_attendanceId_modify").validatebox({
					required : true,
					missingMessage : "请输入记录编号",
					editable: false
				});
				$("#attendance_studentObj_studentNumber_modify").combobox({
					url:"/Student/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"studentNumber",
					textField:"studentName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#attendance_studentObj_studentNumber_modify").combobox("select", attendance.studentObjPri);
						//var data = $("#attendance_studentObj_studentNumber_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#attendance_studentObj_studentNumber_edit").combobox("select", data[0].studentNumber);
						//}
					}
				});
				$("#attendance_courseObj_courseNo_modify").combobox({
					url:"/Course/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"courseNo",
					textField:"courseName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#attendance_courseObj_courseNo_modify").combobox("select", attendance.courseObjPri);
						//var data = $("#attendance_courseObj_courseNo_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#attendance_courseObj_courseNo_edit").combobox("select", data[0].courseNo);
						//}
					}
				});
				$("#attendance_timeInfoObj_timeInfoId_modify").combobox({
					url:"/TimeInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"timeInfoId",
					textField:"timeInfoName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#attendance_timeInfoObj_timeInfoId_modify").combobox("select", attendance.timeInfoObjPri);
						//var data = $("#attendance_timeInfoObj_timeInfoId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#attendance_timeInfoObj_timeInfoId_edit").combobox("select", data[0].timeInfoId);
						//}
					}
				});
				$("#attendance_attendanceStateObj_stateId_modify").combobox({
					url:"/AttendanceState/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"stateId",
					textField:"stateName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#attendance_attendanceStateObj_stateId_modify").combobox("select", attendance.attendanceStateObjPri);
						//var data = $("#attendance_attendanceStateObj_stateId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#attendance_attendanceStateObj_stateId_edit").combobox("select", data[0].stateId);
						//}
					}
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#attendanceModifyButton").click(function(){ 
		if ($("#attendanceModifyForm").form("validate")) {
			$("#attendanceModifyForm").form({
			    url:"Attendance/update/" + $("#attendance_attendanceId_modify").val(),
			    onSubmit: function(){
					if($("#attendanceEditForm").form("validate"))  {
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
			$("#attendanceModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
