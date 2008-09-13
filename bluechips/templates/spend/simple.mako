<%inherit file="/base.mako"/>

<%!
import bluechips.widgets.spend as forms
%>

<p>Want to ${h.link_to('do something more complicated', h.url_for(action='complex'))}?</p>

${forms.simple_spend_form(c.expenditure)}
