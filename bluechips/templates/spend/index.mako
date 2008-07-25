<%inherit file="/base.mako"/>

<%!
import bluechips.widgets.spend as forms
%>

${forms.new_spend_form(c.expenditure, action=h.url_for(action='update'))}
