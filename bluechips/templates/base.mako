<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>${self.title()}</title>
    ${h.stylesheet_link('/style/main.css')}
    ${h.javascript_link('/script/jquery-1.2.6.min.js')}
    ${h.javascript_link('/script/expense_list.js')}
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

<%def name="listSplit(e, splits)">
<ul class="split split_${e.id}">
% for s in splits:
  <li class="split_block">
    <span class="split_name split_name_${e.id}" id="split_name_${e.id}.${s.id}">${s.account.username}</span>
    <span class="split_amount split_amount_${e.id}" id="split_amount_${e.id}.${s.id}">${s.amount}</span>
  </li>
% endfor
</ul>
</%def>

<%def name="listExpenditures(es)">
<table>
    <tr>
        <th></th>
        <th>Date</th>
        <th>Description</th>
        <th>Total Amount</th>
        <th>Debitors</th>
        <th>Creditors</th>
        <th></th>
    </tr>
    % for e in es:
    <tr class="compact expenditure" id="e_${e.id}">
        % if len(e.credits) == 1 and len(e.debits) == 1:
        <td>&nbsp;</td>
        % else:
        <td><img src="/images/contracted.gif" height="11" width="11" class="expand_button" /></td>
        % endif
        <td>${e.date}</td>
        <td>${e.description}</td>
        <td>${sum(c.amount for c in e.credits)}</td>
        
        % if len(e.debits) == 1:
        <td>${e.debits[0].account.username}</td>
        % else:
        <td>${listSplit(e, e.debits)}</td>
        % endif
        
        % if len(e.credits) == 1:
        <td>${e.credits[0].account.username}</td>
        % else:
        <td>${listSplit(e, e.credits)}</td>
        % endif
        
        <td>${h.link_to('Edit', h.url_for(controller='spend', 
                                          action='edit',
                                          id=e.id))}</td>
    </tr>
    % endfor
</table>
</%def>
