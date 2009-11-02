<%inherit file="/base.mako"/>

<%!
import bluechips.widgets.spend as forms
%>

% if c.id != '':
<p>Want to ${h.link_to('change how this expenditure is divided up', h.url_for(controller='spend', action='split', id=c.id))}?</p>
% endif

${forms.new_spend_form(c.expenditure, action=h.url_for(action='update')) | n}
