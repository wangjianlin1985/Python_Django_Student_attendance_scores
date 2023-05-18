$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/ScoreInfo/update/" + $("#scoreInfo_scoreId_modify").val(),
		type : "get",
		data : {
			//scoreId : $("#scoreInfo_scoreId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (scoreInfo, response, status) {
			$.messager.progress("close");
			if (scoreInfo) { 
				$("#scoreInfo_scoreId_modify").val(scoreInfo.scoreId);
				$("#scoreInfo_scoreId_modify").validatebox({
					required : true,
					missingMessage : "请输入成绩编号",
					editable: false
				});
				$("#scoreInfo_studentNumber_studentNumber_modify").combobox({
					url:"/Student/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"studentNumber",
					textField:"studentName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#scoreInfo_studentNumber_studentNumber_modify").combobox("select", scoreInfo.studentNumberPri);
						//var data = $("#scoreInfo_studentNumber_studentNumber_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#scoreInfo_studentNumber_studentNumber_edit").combobox("select", data[0].studentNumber);
						//}
					}
				});
				$("#scoreInfo_courseNo_courseNo_modify").combobox({
					url:"/Course/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"courseNo",
					textField:"courseName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#scoreInfo_courseNo_courseNo_modify").combobox("select", scoreInfo.courseNoPri);
						//var data = $("#scoreInfo_courseNo_courseNo_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#scoreInfo_courseNo_courseNo_edit").combobox("select", data[0].courseNo);
						//}
					}
				});
				$("#scoreInfo_termId_termId_modify").combobox({
					url:"/TermInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"termId",
					textField:"termName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#scoreInfo_termId_termId_modify").combobox("select", scoreInfo.termIdPri);
						//var data = $("#scoreInfo_termId_termId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#scoreInfo_termId_termId_edit").combobox("select", data[0].termId);
						//}
					}
				});
				$("#scoreInfo_score_modify").val(scoreInfo.score);
				$("#scoreInfo_score_modify").validatebox({
					required : true,
					validType : "number",
					missingMessage : "请输入成绩得分",
					invalidMessage : "成绩得分输入不对",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#scoreInfoModifyButton").click(function(){ 
		if ($("#scoreInfoModifyForm").form("validate")) {
			$("#scoreInfoModifyForm").form({
			    url:"ScoreInfo/update/" + $("#scoreInfo_scoreId_modify").val(),
			    onSubmit: function(){
					if($("#scoreInfoEditForm").form("validate"))  {
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
			$("#scoreInfoModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
