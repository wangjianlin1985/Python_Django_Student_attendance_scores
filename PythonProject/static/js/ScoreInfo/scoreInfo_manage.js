var scoreInfo_manage_tool = null; 
$(function () { 
	initScoreInfoManageTool(); //建立ScoreInfo管理对象
	scoreInfo_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#scoreInfo_manage").datagrid({
		url : '/ScoreInfo/list',
		queryParams: {
			"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
		},
		fit : true,
		fitColumns : true,
		striped : true,
		rownumbers : true,
		border : false,
		pagination : true,
		pageSize : 5,
		pageList : [5, 10, 15, 20, 25],
		pageNumber : 1,
		sortName : "scoreId",
		sortOrder : "desc",
		toolbar : "#scoreInfo_manage_tool",
		columns : [[
			{
				field : "scoreId",
				title : "成绩编号",
				width : 70,
			},
			{
				field : "studentNumber",
				title : "学生姓名",
				width : 140,
			},
			{
				field : "courseNo",
				title : "课程名称",
				width : 140,
			},
			{
				field : "termId",
				title : "所在学期",
				width : 140,
			},
			{
				field : "score",
				title : "成绩得分",
				width : 70,
			},
		]],
	});

	$("#scoreInfoEditDiv").dialog({
		title : "修改管理",
		top: "50px",
		width : 700,
		height : 515,
		modal : true,
		closed : true,
		iconCls : "icon-edit-new",
		buttons : [{
			text : "提交",
			iconCls : "icon-edit-new",
			handler : function () {
				if ($("#scoreInfoEditForm").form("validate")) {
					//验证表单 
					if(!$("#scoreInfoEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#scoreInfoEditForm").form({
						    url:"/ScoreInfo/update/" + $("#scoreInfo_scoreId_edit").val(),
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
						    	console.log(data);
			                	var obj = jQuery.parseJSON(data);
			                    if(obj.success){
			                        $.messager.alert("消息","信息修改成功！");
			                        $("#scoreInfoEditDiv").dialog("close");
			                        scoreInfo_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#scoreInfoEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#scoreInfoEditDiv").dialog("close");
				$("#scoreInfoEditForm").form("reset"); 
			},
		}],
	});
});

function initScoreInfoManageTool() {
	scoreInfo_manage_tool = {
		init: function() {
			$.ajax({
				url : "/Student/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#studentNumber_studentNumber_query").combobox({ 
					    valueField:"studentNumber",
					    textField:"studentName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{studentNumber:"",studentName:"不限制"});
					$("#studentNumber_studentNumber_query").combobox("loadData",data); 
				}
			});
			$.ajax({
				url : "/Course/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#courseNo_courseNo_query").combobox({ 
					    valueField:"courseNo",
					    textField:"courseName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{courseNo:"",courseName:"不限制"});
					$("#courseNo_courseNo_query").combobox("loadData",data); 
				}
			});
			$.ajax({
				url : "/TermInfo/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#termId_termId_query").combobox({ 
					    valueField:"termId",
					    textField:"termName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{termId:0,termName:"不限制"});
					$("#termId_termId_query").combobox("loadData",data); 
				}
			});
		},
		reload : function () {
			$("#scoreInfo_manage").datagrid("reload");
		},
		redo : function () {
			$("#scoreInfo_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#scoreInfo_manage").datagrid("options").queryParams;
			queryParams["studentNumber.studentNumber"] = $("#studentNumber_studentNumber_query").combobox("getValue");
			queryParams["courseNo.courseNo"] = $("#courseNo_courseNo_query").combobox("getValue");
			queryParams["termId.termId"] = $("#termId_termId_query").combobox("getValue");
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#scoreInfo_manage").datagrid("options").queryParams=queryParams; 
			$("#scoreInfo_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#scoreInfoQueryForm").form({
			    url:"/ScoreInfo/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#scoreInfoQueryForm").submit();
		},
		remove : function () {
			var rows = $("#scoreInfo_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var scoreIds = [];
						for (var i = 0; i < rows.length; i ++) {
							scoreIds.push(rows[i].scoreId);
						}
						$.ajax({
							type : "POST",
							url : "/ScoreInfo/deletes",
							data : {
								scoreIds : scoreIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#scoreInfo_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#scoreInfo_manage").datagrid("loaded");
									$("#scoreInfo_manage").datagrid("load");
									$("#scoreInfo_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#scoreInfo_manage").datagrid("loaded");
									$("#scoreInfo_manage").datagrid("load");
									$("#scoreInfo_manage").datagrid("unselectAll");
									$.messager.alert("消息",data.message);
								}
							},
						});
					}
				});
			} else {
				$.messager.alert("提示", "请选择要删除的记录！", "info");
			}
		},
		edit : function () {
			var rows = $("#scoreInfo_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/ScoreInfo/update/" + rows[0].scoreId,
					type : "get",
					data : {
						//scoreId : rows[0].scoreId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (scoreInfo, response, status) {
						$.messager.progress("close");
						if (scoreInfo) { 
							$("#scoreInfoEditDiv").dialog("open");
							$("#scoreInfo_scoreId_edit").val(scoreInfo.scoreId);
							$("#scoreInfo_scoreId_edit").validatebox({
								required : true,
								missingMessage : "请输入成绩编号",
								editable: false
							});
							$("#scoreInfo_studentNumber_studentNumber_edit").combobox({
								url:"/Student/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"studentNumber",
							    textField:"studentName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#scoreInfo_studentNumber_studentNumber_edit").combobox("select", scoreInfo.studentNumberPri);
									//var data = $("#scoreInfo_studentNumber_studentNumber_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#scoreInfo_studentNumber_studentNumber_edit").combobox("select", data[0].studentNumber);
						            //}
								}
							});
							$("#scoreInfo_courseNo_courseNo_edit").combobox({
								url:"/Course/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"courseNo",
							    textField:"courseName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#scoreInfo_courseNo_courseNo_edit").combobox("select", scoreInfo.courseNoPri);
									//var data = $("#scoreInfo_courseNo_courseNo_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#scoreInfo_courseNo_courseNo_edit").combobox("select", data[0].courseNo);
						            //}
								}
							});
							$("#scoreInfo_termId_termId_edit").combobox({
								url:"/TermInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"termId",
							    textField:"termName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#scoreInfo_termId_termId_edit").combobox("select", scoreInfo.termIdPri);
									//var data = $("#scoreInfo_termId_termId_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#scoreInfo_termId_termId_edit").combobox("select", data[0].termId);
						            //}
								}
							});
							$("#scoreInfo_score_edit").val(scoreInfo.score);
							$("#scoreInfo_score_edit").validatebox({
								required : true,
								validType : "number",
								missingMessage : "请输入成绩得分",
								invalidMessage : "成绩得分输入不对",
							});
						} else {
							$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
						}
					}
				});
			} else if (rows.length == 0) {
				$.messager.alert("警告操作！", "编辑记录至少选定一条数据！", "warning");
			}
		},
	};
}
