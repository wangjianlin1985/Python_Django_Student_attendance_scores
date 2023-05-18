$(function () {
	$("#scoreInfo_score").validatebox({
		required : true,
		validType : "number",
		missingMessage : '请输入成绩得分',
		invalidMessage : '成绩得分输入不对',
	});

	//单击添加按钮
	$("#scoreInfoAddButton").click(function () {
		//验证表单 
		if(!$("#scoreInfoAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#scoreInfoAddForm").form({
			    url:"/ScoreInfo/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#scoreInfoAddForm").form("validate"))  { 
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
                        $("#scoreInfoAddForm").form("clear");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#scoreInfoAddForm").submit();
		}
	});

	//单击清空按钮
	$("#scoreInfoClearButton").click(function () { 
		//$("#scoreInfoAddForm").form("clear"); 
		location.reload()
	});
});
