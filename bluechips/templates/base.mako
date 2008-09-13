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
    <div id="nav">
      <ul>
        <li>${h.link_to('Dashboard', h.url_for(controller='status',
                                               action='index',
                                               id=None))}</li>
        <li>${h.link_to('Expense', h.url_for(controller='spend',
                                             action='index',
                                             id=None))}</li>
        <li>${h.link_to('Transfer', h.url_for(controller='transfer',
                                              action='index',
                                              id=None))}</li>
        <li>${h.link_to('History', h.url_for(controller='history',
                                             action='index',
                                             id=None))}</li>
      </ul>
    </div>
    <div id="content">
      ${next.body()}
    </div>
  </body>
</html>

<%def name="title()">BlueChips
% if c.title != '':
  :: ${c.title}
% endif
</%def>

<%def name="listExpenditures(es)">
<table>
    <tr>
        <th>Date</th>
        <th>Description</th>
        <th>Total Amount</th>
        <th>Debitors</th>
        <th>Creditors</th>
        <th></th>
    </tr>
    % for e in es:
    <tr>
        <td>${e.date}</td>
        <td>${e.description}</td>
        <td>${sum(c.amount for c in e.credits)}</td>
        <td>${', '.join(c.account.username for c in e.credits)}</td>
        <td>${', '.join(d.account.username for d in e.debits)}</td>
        <td>${h.link_to('Edit', h.url_for(controller='spend', 
                                          action='edit',
                                          id=e.id))}</td>
    </tr>
    % endfor
</table>
</%def>
