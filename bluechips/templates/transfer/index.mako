<%inherit file="/base.mako"/>

<%def name="title()">${parent.title()} :: Add a New Transfer</%def>
<%!
import bluechips.widgets.transfer as forms
%>

${forms.new_transfer_form(c.transfer, action=h.url_for(action='new'))}
