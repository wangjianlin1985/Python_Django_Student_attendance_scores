var attendance_manage_tool = null; 
$(function () { 
	initAttendanceManageTool(); //建立Attendance管理对象
	attendance_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#attendance_manage").datagrid({
		url : '/Attendance/list',
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
		sortName : "attendanceId",
		sortOrder : "desc",
		toolbar : "#attendance_manage_tool",
		columns : [[
			{
				field : "attendanceId",
				title : "记录编号",
				width : 70,
			},
			{
				field : "studentObj",
				title : "学生",
				width : 140,
			},
			{
				field : "courseObj",
				title : "课程",
				width : 140,
			},
			{
				field : "timeInfoObj",
				title : "时间",
				width : 140,
			},
			{
				field : "attendanceStateObj",
				title : "状态",
				width : 140,
			},
		]],
	});

	$("#attendanceEditDiv").dialog({
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
				if ($("#attendanceEditForm").form("validate")) {
					//验证表单 
					if(!$("#attendanceEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#attendanceEditForm").form({
						    url:"/Attendance/update/" + $("#attendance_attendanceId_edit").val(),
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
						    	console.log(data);
			                	var obj = jQuery.parseJSON(data);
			                    if(obj.success){
			                        $.messager.alert("消息","信息修改成功！");
			                        $("#attendanceEditDiv").dialog("close");
			                        attendance_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#attendanceEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#attendanceEditDiv").dialog("close");
				$("#attendanceEditForm").form("reset"); 
			},
		}],
	});
});

function initAttendanceManageTool() {
	attendance_manage_tool = {
		init: function() {
			$.ajax({
				url : "/Student/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#studentObj_studentNumber_query").combobox({ 
					    valueField:"studentNumber",
					    textField:"studentName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{studentNumber:"",studentName:"不限制"});
					$("#studentObj_studentNumber_query").combobox("loadData",data); 
				}
			});
			$.ajax({
				url : "/Course/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#courseObj_courseNo_query").combobox({ 
					    valueField:"courseNo",
					    textField:"courseName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{courseNo:"",courseName:"不限制"});
					$("#courseObj_courseNo_query").combobox("loadData",data); 
				}
			});
			$.ajax({
				url : "/TimeInfo/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#timeInfoObj_timeInfoId_query").combobox({ 
					    valueField:"timeInfoId",
					    textField:"timeInfoName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{timeInfoId:0,timeInfoName:"不限制"});
					$("#timeInfoObj_timeInfoId_query").combobox("loadData",data); 
				}
			});
			$.ajax({
				url : "/AttendanceState/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#attendanceStateObj_stateId_query").combobox({ 
					    valueField:"stateId",
					    textField:"stateName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{stateId:"",stateName:"不限制"});
					$("#attendanceStateObj_stateId_query").combobox("loadData",data); 
				}
			});
		},
		reload : function () {
			$("#attendance_manage").datagrid("reload");
		},
		redo : function () {
			$("#attendance_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#attendance_manage").datagrid("options").queryParams;
			queryParams["studentObj.studentNumber"] = $("#studentObj_studentNumber_query").combobox("getValue");
			queryParams["courseObj.courseNo"] = $("#courseObj_courseNo_query").combobox("getValue");
			queryParams["timeInfoObj.timeInfoId"] = $("#timeInfoObj_timeInfoId_query").combobox("getValue");
			queryParams["attendanceStateObj.stateId"] = $("#attendanceStateObj_stateId_query").combobox("getValue");
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#attendance_manage").datagrid("options").queryParams=queryParams; 
			$("#attendance_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#attendanceQueryForm").form({
			    url:"/Attendance/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#attendanceQueryForm").submit();
		},
		remove : function () {
			var rows = $("#attendance_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var attendanceIds = [];
						for (var i = 0; i < rows.length; i ++) {
							attendanceIds.push(rows[i].attendanceId);
						}
						$.ajax({
							type : "POST",
							url : "/Attendance/deletes",
							data : {
								attendanceIds : attendanceIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#attendance_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#attendance_manage").datagrid("loaded");
									$("#attendance_manage").datagrid("load");
									$("#attendance_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#attendance_manage").datagrid("loaded");
									$("#attendance_manage").datagrid("load");
									$("#attendance_manage").datagrid("unselectAll");
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
			var rows = $("#attendance_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/Attendance/update/" + rows[0].attendanceId,
					type : "get",
					data : {
						//attendanceId : rows[0].attendanceId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (attendance, response, status) {
						$.messager.progress("close");
						if (attendance) { 
							$("#attendanceEditDiv").dialog("open");
							$("#attendance_attendanceId_edit").val(attendance.attendanceId);
							$("#attendance_attendanceId_edit").validatebox({
								required : true,
								missingMessage : "请输入记录编号",
								editable: false
							});
							$("#attendance_studentObj_studentNumber_edit").combobox({
								url:"/Student/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"studentNumber",
							    textField:"studentName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#attendance_studentObj_studentNumber_edit").combobox("select", attendance.studentObjPri);
									//var data = $("#attendance_studentObj_studentNumber_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#attendance_studentObj_studentNumber_edit").combobox("select", data[0].studentNumber);
						            //}
								}
							});
							$("#attendance_courseObj_courseNo_edit").combobox({
								url:"/Course/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"courseNo",
							    textField:"courseName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#attendance_courseObj_courseNo_edit").combobox("select", attendance.courseObjPri);
									//var data = $("#attendance_courseObj_courseNo_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#attendance_courseObj_courseNo_edit").combobox("select", data[0].courseNo);
						            //}
								}
							});
							$("#attendance_timeInfoObj_timeInfoId_edit").combobox({
								url:"/TimeInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"timeInfoId",
							    textField:"timeInfoName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#attendance_timeInfoObj_timeInfoId_edit").combobox("select", attendance.timeInfoObjPri);
									//var data = $("#attendance_timeInfoObj_timeInfoId_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#attendance_timeInfoObj_timeInfoId_edit").combobox("select", data[0].timeInfoId);
						            //}
								}
							});
							$("#attendance_attendanceStateObj_stateId_edit").combobox({
								url:"/AttendanceState/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"stateId",
							    textField:"stateName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#attendance_attendanceStateObj_stateId_edit").combobox("select", attendance.attendanceStateObjPri);
									//var data = $("#attendance_attendanceStateObj_stateId_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#attendance_attendanceStateObj_stateId_edit").combobox("select", data[0].stateId);
						            //}
								}
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
