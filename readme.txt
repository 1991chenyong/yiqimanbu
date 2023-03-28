YAML格式用例的约定
1. 必须包含一级关键字：name,request,validate,project
2. 在request关键字下必须包括：method, url, data
3. 提取变量使用一级关键字extract，支持json提取和正则表达式提取，使用{{}}取值
4. 可以使用热加载的方式调用debug_talk.py中的DebugTalk类里面的方法，通过${}调用
5. 支持codes,equals和contains三种断言
6. 使用parameters做csv文件的数据驱动，通过$csv{appid}这种格式取值
parameters:
    name-appid-grant_type-secret-eq_str: data/get_token_data.csv

--------------------------
注意事项
1. 本项目包含两个平台，编写用例时通过project字段区分

data与json2个参数，类型既可以是str，也可以是dict
区别如下：

1、不管json是str还是dict，如果不指定headers中的content-type，默认为application/json
2、data参数为dict时，如果不指定content-type，默认为application/x-www-form-urlencoded，相当于普通form表单提交的形式，此时数据可以从request.POST里面获取，
而request.body的内容则为a=1&b=2的这种形式，注意，即使指定content-type=application/json，request.body的值也是类似于a=1&b=2，所以并不能用json.loads(request.body.decode())得到想要的值
3、data参数为str时，如果不指定content-type，默认为application/json
4、用data参数提交数据时，request.body的内容则为a=1&b=2的这种形式，用json参数提交数据时，request.body的内容则为'{"a": 1, "b": 2}'的这种形式
下图是data方式
