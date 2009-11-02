<%inherit file="/base.mako"/>

<%!
import bluechips.widgets.transfer as forms
%>

${forms.new_transfer_form(c.transfer, action=h.url_for(action='update')) | n}
