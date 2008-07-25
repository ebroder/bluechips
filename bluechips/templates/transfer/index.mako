<%inherit file="/base.mako"/>

<%def name="title()">${parent.title()} :: ${c.title}</%def>
<%!
import bluechips.widgets.transfer as forms
%>

${forms.new_transfer_form(c.transfer, action=h.url_for(action='update'))}
