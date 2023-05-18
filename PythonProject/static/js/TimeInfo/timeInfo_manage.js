var timeInfo_manage_tool = null; 
$(function () { 
	initTimeInfoManageTool(); //建立TimeInfo管理对象
	timeInfo_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#timeInfo_manage").datagrid({
		url : '/TimeInfo/list',
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
		sortName : "timeInfoId",
		sortOrder : "desc",
		toolbar : "#timeInfo_manage_tool",
		columns : [[
			{
				field : "timeInfoId",
				title : "记录编号",
				width : 70,
			},
			{
				field : "timeInfoName",
				title : "学时名称",
				width : 140,
			},
		]],
	});

	$("#timeInfoEditDiv").dialog({
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
				if ($("#timeInfoEditForm").form("validate")) {
					//验证表单 
					if(!$("#timeInfoEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#timeInfoEditForm").form({
						    url:"/TimeInfo/update/" + $("#timeInfo_timeInfoId_edit").val(),
						    onSubmit: function(){
								if($("#timeInfoEditForm").form("validate"))  {
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
			                        $("#timeInfoEditDiv").dialog("close");
			                        timeInfo_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#timeInfoEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#timeInfoEditDiv").dialog("close");
				$("#timeInfoEditForm").form("reset"); 
			},
		}],
	});
});

function initTimeInfoManageTool() {
	timeInfo_manage_tool = {
		init: function() {
		},
		reload : function () {
			$("#timeInfo_manage").datagrid("reload");
		},
		redo : function () {
			$("#timeInfo_manage").datagrid("unselectAll");
		},
		search: function() {
			$("#timeInfo_manage").datagrid("options").queryParams=queryParams; 
			$("#timeInfo_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#timeInfoQueryForm").form({
			    url:"/TimeInfo/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#timeInfoQueryForm").submit();
		},
		remove : function () {
			var rows = $("#timeInfo_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var timeInfoIds = [];
						for (var i = 0; i < rows.length; i ++) {
							timeInfoIds.push(rows[i].timeInfoId);
						}
						$.ajax({
							type : "POST",
							url : "/TimeInfo/deletes",
							data : {
								timeInfoIds : timeInfoIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#timeInfo_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#timeInfo_manage").datagrid("loaded");
									$("#timeInfo_manage").datagrid("load");
									$("#timeInfo_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#timeInfo_manage").datagrid("loaded");
									$("#timeInfo_manage").datagrid("load");
									$("#timeInfo_manage").datagrid("unselectAll");
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
			var rows = $("#timeInfo_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/TimeInfo/update/" + rows[0].timeInfoId,
					type : "get",
					data : {
						//timeInfoId : rows[0].timeInfoId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (timeInfo, response, status) {
						$.messager.progress("close");
						if (timeInfo) { 
							$("#timeInfoEditDiv").dialog("open");
							$("#timeInfo_timeInfoId_edit").val(timeInfo.timeInfoId);
							$("#timeInfo_timeInfoId_edit").validatebox({
								required : true,
								missingMessage : "请输入记录编号",
								editable: false
							});
							$("#timeInfo_timeInfoName_edit").val(timeInfo.timeInfoName);
							$("#timeInfo_timeInfoName_edit").validatebox({
								required : true,
								missingMessage : "请输入学时名称",
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
