(function (jq) {
        var requestURL;  //将公共参数提取出来

        //为字符串创建format方法，用于字符串格式化
        String.prototype.format = function (args) {
            return this.replace(/\{(\w+)\}/g, function (s, i) {
                return args[i];
            });
        };

        function init() {
            //获取显示的列
            //获取数据
            $.ajax({
                url: requestURL,
                type: 'GET',
                dataType: 'JSON',
                success: function (arg) {
                    if(arg.status) {
                        createTablehead(arg.data.table_config);
                        createTablebody(arg.data.table_config, arg.data.data_list);
                    }else{
                        alert(arg.message);
                    }
                }
            });
        }

        function createTablehead(config) {
            /*
            config = [
                {
                    'title': '主机名',
                    'display': '1',
                },
                {
                    'title': '端口',
                    'display': '1',
                },

            ]
            通过拿到的配置文件，在thead标签内自动生成tr、th标签，
            <tr>
                <td>主机名</td>
                <td>端口</td>
            </tr>
            */

            //console.log(config);
            var tr = document.createElement('tr');
            $.each(config,function (k,v) {
                //k 为被循环对象config的元素下下标， v为对象中的元素
                if(v.display){
                    var th = document.createElement('th');
                    th.innerHTML = v.title;
                    $(tr).append(th);
                }
            })
            $("#thead").append(tr);
        }

        function createTablebody(table_config, data_list) {
            $.each(data_list, function (k1, row) {
                // row1 = {'hostname': 'h1.com', 'port':'22'} ...
                var tr = document.createElement('tr');
                $.each(table_config, function (k2, config_item) {
                    if(config_item.display){
                        var td = document.createElement('td');

                        //定制表格内容
                        // td.innerHTML = row[config_item.q];
                        var kwargs = {};
                        $.each(config_item.text.kwargs, function (key,value) {
                            //key 为字典的键，value 为字典的值

                            if(value.startsWith('@')){
                                var temp = value.substring(1, value.length);
                                kwargs[key] = row[temp];  //kwargs = {'0', 'h1.com',...}
                            }else{
                                kwargs[key] = value;
                            };
                        })
                        td.innerHTML = config_item.text.content.format(kwargs);

                        //定制样式
                        $.each(config_item.attr, function (key, value) {
                            if(value.startsWith('@')){
                                var temp = value.substring(1, value.length);
                                td.setAttribute(key,row[temp]);
                            }else{
                                td.setAttribute(key,value);
                            };
                        });

                        $(tr).append(td);
                    }
                });
                $('#tbody').append(tr);
            });
        }

        $.extend({
            'table_init': function (url) {
                requestURL = url;
                init();
            },
        })

})(jQuery)