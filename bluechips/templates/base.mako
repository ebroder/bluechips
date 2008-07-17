<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>${self.title()}</title>
    ${h.stylesheet_link('/css/main.css')}
  </head>
  <body>
    <h1>${self.title()}</h1>
    <% messages = h.flash.pop_messages() %>
    % if messages:
    <ul id="flash-messages">
    % for message in messages:
        <li>${message}</li>
    % endfor
    </ul>
    % endif
    <div id="content">
      ${next.body()}
    </div>
  </body>
</html>

<%def name="title()">BlueChips</%def>

<%def name="listExpenditures(es)">
<table>
    <tr>
        <th>Date</th>
        <th>Spender</th>
        <th>Description</th>
        <th>Amount</th>
    </tr>
    % for e in es:
    <tr>
        <td>${e.date}</td>
        <td>${e.spender.name}</td>
        <td>${e.description}</td>
        <td>$${h.round_currency(e.amount)}</td>
    </tr>
    % endfor
</table>
</%def>

<%def name="listTransfers(ts)">
<table>
    <tr>
        <th>Date</th>
        <th>From</th>
        <th>To</th>
        <th>Description</th>
        <th>Amount</th>
    </tr>
    % for t in ts:
    <tr>
        <td>${t.date}</td>
        <td>${t.debtor.name}</td>
        <td>${t.creditor.name}</td>
        <td>${t.description}</td>
        <td>$${h.round_currency(t.amount)}</td>
    </tr>
    % endfor
</table>
</%def>
