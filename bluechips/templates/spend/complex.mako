<%inherit file="/base.mako"/>

<%!
import bluechips.widgets.spend as forms
%>

<p>For debits and credits, enter a percentage, a dollar amount, or
anything else. The total shares don't have to add to 100 or the total
amount of the transaction.</p>

${forms.complex_spend_form()}
