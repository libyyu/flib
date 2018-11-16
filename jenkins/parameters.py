# -*- coding: utf-8 -*-
"""
生成Jenkins控件
"""
import sys
import argparse

class JenkinsParameter(object):
    """
    Jenkins上的控件
    """
    table_template = """
        <table width="100%" class="parameters">
            <tbody>
            {rows}
            </tbody>
        </table>
    """
    def __init__(self, fields = []):
        self.registerFields(fields)
    def registerFields(self, fields):
        self.fields = fields
    def toFile(self, file="jenkins.html"):
        head = """
                <head>
                    <meta http-equiv=Content-Type content="text/html; charset=utf-8">
                    <title>Jenkins Parameters</title>
                </head>
                """
        with open(file, "w") as f:
            f.write(head + self.toJenkins())
    def toJenkins(self):
        rows = ""
        for field in self.fields:
            rows += field.toJenkins()
        return self.table_template.format(rows=rows)
    def fromJenkins(self, params):
        result = {}
        pos = 0
        for field in self.fields:
            if isinstance(field, InputFiled):
                (name, value) = field.fromJenkins(params, pos)
                result[name] = value
                pos += 1
                continue
            elif isinstance(field, CheckBoxField):
                (name, value) = field.fromJenkins(params, pos)
                result[name] = value
                pos += 1
                continue
            elif isinstance(field, SelectField):
                (name, value, pos) = field.fromJenkins(params, pos)
                result[name] = value
                continue
            elif isinstance(field, GroupField):
                (name, value, pos) = field.fromJenkins(params, pos)
                result[name] = value
                continue
            else:
                continue
        return result

class Field(object):
    """
    Jenkins上的一个参数
    """
    def __init__(self, name, description):
        """
        构造一个option
        :param name:变量名称
        :param description:变量描述
        """
        self.name = name
        self.description = description
    def toJenkins(self):
        raise Exception("can not call interface Field.toJenkins")
    def fromJenkins(self, params, pos):
        raise Exception("can not call interface Field.fromJenkins")

class PartLineField(Field):
    """
    Jenksin上的一个横向分割线
    """
    def __init__(self, description = "", **kwargs):
        Field.__init__(self, "PARTLINE", description=description)
    def toJenkins(self):
        return """<tr>
                    <td class="setting-leftspace">&nbsp;</td>
                    <td><div>
                        <hr style="filter: alpha(opacity=100,finishopacity=0,style=2)" align="left" width="100%;" color=#987cb9 size=8>
                        <br/>
                        <hr style="filter: alpha(opacity=100,finishopacity=0,style=2)" align="left" width="100%;" color=#987cb9 size=8>
                    </div></td>
                    <td><div>
                        <hr style="filter: alpha(opacity=100,finishopacity=0,style=2)" align="left" width="100%;" color=#987cb9 size=8>
                        {desc}<br/>
                        <hr style="filter: alpha(opacity=100,finishopacity=0,style=2)" align="left" width="100%;" color=#987cb9 size=8>
                    </div></td>
                    <td></td>
                </tr>
                """.format(desc=self.description)

class GroupField(Field):
    """
        控件组
    """
    def __init__(self, name, description = "", fields = None, **kwargs):
        Field.__init__(self, name, description=description)
        self.fields = fields or []
        self.kwargs = kwargs
        self.init_value = None
    @property
    def Fields(self):
        return self.fields
    def addField(self, field):
        self.fields.append(field)
    def __add__(self, field):
        self.addField(field)
        return self
    def toJenkins(self):
        rows = PartLineField(description = self.description).toJenkins()
        for field in self.fields:
            rows += field.toJenkins()
        return rows
    def fromJenkins(self, params, pos):
        result = {}
        for field in self.fields:
            if isinstance(field, InputFiled):
                (name, value) = field.fromJenkins(params, pos)
                result[name] = value
                pos += 1
                continue
            elif isinstance(field, CheckBoxField):
                (name, value) = field.fromJenkins(params, pos)
                result[name] = value
                pos += 1
                continue
            elif isinstance(field, SelectField):
                (name, value, pos) = field.fromJenkins(params, pos)
                result[name] = value
                continue
            elif isinstance(field, GroupField):
                (name, value, pos) = field.fromJenkins(params, pos)
                result[name] = value
                continue
            else:
                continue
        self.init_value = {}
        self.init_value[self.name] = result
        return (self.name, result, pos)
    def __str__(self):
        return """{self}.init_value={init_value}""".format(self=self, init_value=self.init_value)

class InputFiled(Field):
    """
    Jenksin上的一个输入框
    """
    def __init__(self, name, description = "", init_value = "", match="", errMsgwhenNotMatch="", readonly=False, init_func = None, **kwargs):
        Field.__init__(self, name, description=description)
        self.input_type = "text"
        self.class_style = "setting-input"
        self.init_value = init_value
        self.init_func = init_func
        self.kwargs = kwargs
        self.readonly=readonly
        self.match = match
        self.errMsgwhenNotMatch = errMsgwhenNotMatch
    def __checkMatch(self):
        """
        限制输入
        """
        if not self.match: return ""
        return """
                        if(obj.value.length==0){{
                            return;
                        }}
                        else if(obj.value.match({match}))
                            return;
                        else {{
                            {alert};
                            document.execCommand('Undo');
                        }}
                """.format(match=self.match, alert='''alert("{err_msg}")'''.format(err_msg=self.errMsgwhenNotMatch))
    def __genLimit(self):
        return ("""onkeyup="onkeyup_{param}(this)" onafterpaste="onkeyup_{param}(this)" """.format(param=self.name), 
                """<script type="text/javascript">
                       function onkeyup_{param}(obj) {{
                            {check}
                       }}
                    </script>""".format(param=self.name, check=self.__checkMatch()))
    def toJenkins(self):
        (onlimit, script) = self.__genLimit()
        return """
                <tr>
                    <td class="setting-leftspace">&nbsp;</td>
                    <td class="setting-name">{param}</td>
                    <td class="setting-main">
                        <input name="value" type="{input_type}" class="{class_style}" value="{value}" {readonly} {onlimit}">
                    </td>
                    <td class="setting-no-help"></td>
                </tr>
                <tr class="validation-error-area">
                    <td colspan="2"></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td colspan="2"></td>
                    <td class="setting-description">{desc}</td>
                    <td></td>
                </tr>
                {script}
            """.format(param=self.name, 
                input_type=self.input_type, 
                class_style=self.class_style, 
                desc=self.description, 
                value=self.init_func(self) if self.init_func else self.init_value,
                readonly='''readonly="readonly"''' if self.readonly else "",
                onlimit=onlimit,
                script=script)
    def fromJenkins(self, params, pos):
        self.init_value = params[pos]
        return (self.name, self.init_value)
    def __str__(self):
        return """{self}.init_value={init_value}""".format(self=self, init_value=self.init_value)

class CheckBoxField(Field):
    """
    Jenkins上的checkbox控件
    """
    def __init__(self, name, description = "", init_value = False, init_func = None, **kwargs):
        Field.__init__(self, name, description=description)
        self.input_type = "checkbox"
        self.class_style = "  "
        self.init_value = "true" if init_value else "false"
        self.init_func = init_func
        self.kwargs = kwargs
    def toJenkins(self):
        if self.init_func:
            value = '''checked="true"''' if self.init_func(self) == "true" else ""
        else:
            value = '''checked="true"''' if self.init_value == "true" else ""
        return """
                <tr>
                    <td class="setting-leftspace">&nbsp;</td>
                    <td class="setting-name">{param}</td>
                    <td class="setting-main">
                        <input name="value" type="{input_type}" class="{class_style}" {value}">
                    </td>
                    <td class="setting-no-help"></td>
                </tr>
                <tr class="validation-error-area">
                    <td colspan="2"></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td colspan="2"></td>
                    <td class="setting-description">{desc}</td>
                    <td></td>
                </tr>
            """.format(param=self.name,
                       input_type=self.input_type,
                       class_style=self.class_style,
                       desc=self.description,
                       value=value)
    def fromJenkins(self, params, pos):
        self.init_value = params[pos]
        return (self.name, self.init_value)
    def __str__(self):
        return """{self}.init_value={init_value}""".format(self=self, init_value=self.init_value)

class SelectField(Field):
    """
    Jenkins下拉选项控件
    """
    def __init__(self, name, description="", init_value="", options = [], multi_select=False, init_func = None, **kwargs):
        Field.__init__(self, name, description=description)
        self.init_value = init_value
        self.init_func = init_func
        self.kwargs = kwargs
        self.multi_select = multi_select
        self.options = options
    @property
    def isMuliSelect(self):
        return self.multi_select
    def __isSelected(self, value):
        if self.init_func:
            selects = self.init_func(self)
        else:
            selects = self.init_value
        if isinstance(selects, list):
            return value in selects
        else:
            return value == selects
    def __genSingleSelect(self):
        options_ = ""
        for option in self.options:
            options_ += """<option value="{param}${name}" {selected}>{name}</option>""".format(param=self.name,
                        name=option,
                        selected='''selected="selected"''' if self.__isSelected(option) else "")
        return """
                <tr>
                    <td class="setting-leftspace">&nbsp;</td>
                    <td class="setting-name">{param}</td>
                    <td class="setting-main">
                        <select name="value">
                            {options}
                        </select>
                    </td>
                    <td class="setting-no-help"></td>
                </tr>
                <tr class="validation-error-area">
                    <td colspan="2"></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td colspan="2"></td>
                    <td class="setting-description">{desc}</td>
                    <td></td>
                </tr>
            """.format(param=self.name, options=options_, desc=self.description)
    def __genMultiSelect(self):
        options_ = ""
        for option in self.options:
            options_ += """
            <tr style="white-space:nowrap">
            <td>
            <input type="checkbox" name="value" alt="{param}${value}" json="{param}${value}" title="{param}${value}" value="{param}${value}" class=" " {checked}>
            <label title="{value}" class="attach-previous">{value}</label>
            {extern_value}
            </td>
            </tr>
            """.format(param=self.name,
                       value=option,
                       checked='''checked="checked"''' if self.__isSelected(option) else "",
                       extern_value=self.kwargs['get_extern_value'](option) if 'get_extern_value' in self.kwargs else "")
        div = """<div style="float: left; overflow-y: auto; padding-right: 25px;" class="dynamic_checkbox">
            <table>
            <tbody>
            {tbody}
            </tbody>
            </table>
            </div>""".format(tbody=options_)
        return """
            <tr>
                <td class="setting-leftspace">&nbsp;</td>
                <td class="setting-name">{param}</td>
                <td class="setting-main">
                    {div}
                </td>
                <td class="setting-no-help"></td>
            </tr>
            <tr class="validation-error-area">
                <td colspan="2"></td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td colspan="2"></td>
                <td class="setting-description">{desc}</td>
                <td></td>
            </tr>
        """.format(param=self.name, div=div, desc=self.description)
    def toJenkins(self):
        if self.multi_select:
            return self.__genMultiSelect()
        else:
            return self.__genSingleSelect()
    def fromJenkins(self, params, pos):
        newpos = pos
        hasFind = False
        for x in xrange(newpos,len(params)):
            if params[x].startswith(self.name + "$"):
                newpos = x
                hasFind = True
                continue
            else:
                break
        if not hasFind:
            if self.isMuliSelect:
                self.init_value = []
            else:
                self.init_value = ""
            return (self.name, self.init_value, pos)
        results = params[pos:newpos+1]
        results = [ x.lstrip(self.name+"$") for x in results ]
        if self.isMuliSelect:
            self.init_value = results
            pos += len(results)
        else:
            self.init_value = results[0] if len(results) >0 else ""
            pos += 1
        return (self.name, self.init_value, pos)
    def __str__(self):
        return """{self}.init_value={init_value}""".format(self=self, init_value=self.init_value)

class FileField(Field):
    """
    文件上传空间
    """
    def __init__(self, name, description = "", init_value = "", accept="", **kwargs):
        """
        :param name:
        :param description:
        :param init_value:
        :param accept:支持的文件格式
        :param kwargs:
        """
        Field.__init__(self, name, description=description)
        self.input_type = "file"
        self.init_value = init_value
        self.accept = accept
        self.kwargs = kwargs
    def toJenkins(self):
        return """
               <tr>
                   <td class="setting-leftspace">&nbsp;</td>
                   <td class="setting-name">{param}</td>
                   <td class="setting-main">
                        <input name="file" type="{input_type}" jsonaware="true" class="{class_style}" {accept} {value}" />
                   </td>
                   <td class="setting-no-help"></td>
               </tr>
               <tr class="validation-error-area">
                    <td colspan="2"></td>
                    <td></td>
                    <td></td>
                </tr>
               <tr>
                   <td colspan="2"></td>
                   <td class="setting-description">{desc}</td>
                   <td></td>
               </tr>
                """.format(param=self.name, input_type=self.input_type, class_style="  ",
                            desc=self.description,
                            accept='''accept="{}"'''.format(self.accept) if self.accept else "",
                            value="")

class FileExtendField(Field):
    """
    文件上传控件
    """
    def __init__(self, name, description = "", init_value = "", accept="", onclick = None, **kwargs):
        """
        :param name:
        :param description:
        :param init_value:
        :param accept:支持的文件格式
        :param kwargs:
        """
        Field.__init__(self, name, description=description)
        self.input_type = "file"
        self.init_value = init_value
        self.accept = accept
        self.onclick = onclick
        self.kwargs = kwargs
    def toJenkins(self):
        return """
               <tr>
                   <td class="setting-leftspace">&nbsp;</td>
                   <td class="setting-name">{param}</td>
                   <td class="setting-main">
                       <input type="text" id="{param}_f_file" readonly="readonly" />
                       <input name="{param}" id="{param}" type="button" value="文件上传" jsonaware="true" class="{class_style}" {accept} {value} onclick="btn_{param}()" />
                       <input name="{param}" type="file" id="{param}_t_file" onchange="{param}_f_file.value=this.value" style="display:none" />
                   </td>
               </tr>
               <tr>
                   <td colspan="2"></td>
                   <td class="setting-description">{desc}</td>
               </tr>
               <script type="text/javascript">
               function btn_{param}() {{
                    {param}_t_file.click();
               }}
               </script>
                """.format(param=self.name, class_style="  ",
                            desc=self.description,
                            accept='''accept="{}"'''.format(self.accept) if self.accept else "",
                            value="",
                            onclick=self.onclick(self) if self.onclick else "")

class TableField(Field):
    """
    二维表控件
    """
    def __init__(self, name, description = "", title = [], datas = [], init_value=None, **kwargs):
        Field.__init__(self, name, description=description)
        self.input_type = "table"
        self.title = title
        self.datas = datas
        self.init_value = init_value
        self.kwargs = kwargs
    def __genHead(self):
        if not self.title: return ""
        options = ""
        for title in self.title:
            options += """
                        <th>{title}</th>
                        """.format(title=title)
        return """<tr>
                    {options}
                 </tr>
                """.format(options=options)
    def __genRow(self, rows):
        options = ""
        for row in rows:
            options += """
                        <td>{row}</td>
                        """.format(row=row)
        return """
                <tr>
                    {options}
                </tr>
                """.format(options=options)
    def __genContent(self):
        if not self.datas: return ""
        rows = ""
        for row in self.datas:
            rows += self.__genRow(row)
        return """
                {rows}
                """.format(rows=rows)
    def __genTable(self):
        return """
                <table border="1" cellspacing="0">
                    <tbody>
                        {head}
                        {content}
                    </tbody>
                </table>
                """.format(head=self.__genHead(), content=self.__genContent())
    def toJenkins(self):
        return """
               <tr>
                   <td class="setting-leftspace">&nbsp;</td>
                   <td class="setting-name">{param}</td>
                   <td class="setting-main">
                       {table}
                   </td>
                   <td class="setting-no-help"></td>
               </tr>
               <tr class="validation-error-area">
                    <td colspan="2"></td>
                    <td></td>
                    <td></td>
                </tr>
               <tr>
                   <td colspan="2"></td>
                   <td class="setting-description">{desc}</td>
                   <td></td>
               </tr>
                """.format(param=self.name, class_style="  ",
                            desc=self.description,
                            table=self.__genTable())

class ImageField(Field):
    def __init__(self, name,description = "", init_value = "", init_func = None,  width = 64, height = 64, **kwargs):
        Field.__init__(self, name, description=description)
        self.init_value = init_value
        self.init_func = init_func
        self.width = width
        self.height = height
        self.kwargs = kwargs
    def toJenkins(self):
        return """
            <tr>
                <td class="setting-leftspace">&nbsp;</td>
                <td class="setting-name">{param}</td>
                <td>
                    <img src="{url}" width="{width}" height="{height}"/>
                </td>
            </tr>
            <tr class="validation-error-area">
                <td colspan="2"></td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td colspan="2"></td>
                <td class="setting-description">{desc}</td>
                <td></td>
            </tr>
            """.format(param=self.name,
                       desc=self.description,
                       width=self.width,
                       height=self.height,
                       url=self.init_func(self) if self.init_func else self.init_value)


