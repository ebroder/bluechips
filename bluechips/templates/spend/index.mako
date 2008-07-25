<%inherit file="/base.mako"/>

<%def name="title()">${parent.title()} :: ${c.title}</%def>
<%!
import bluechips.widgets.spend as forms
%>

${forms.new_spend_form(c.expenditure, action=h.url_for(action='update'))}
