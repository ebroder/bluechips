<%inherit file="/base.mako"/>

<%def name="title()">${parent.title()} :: History</%def>

<h2>Group Expenditures</h2>

${self.listExpenditures(c.expenditures)}

<h2>Transfers</h2>

${self.listTransfers(c.transfers)}
