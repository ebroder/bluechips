<%inherit file="/base.mako"/>

<%def name="title()">${parent.title()} :: Add a New Expenditure</%def>

<%namespace name="forms" module="bluechips.widgets.spend" />

${forms.new_spend_form(action=h.url_for(action='new'))}
