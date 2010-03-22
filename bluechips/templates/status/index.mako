<%inherit file="/base.mako"/>

<div class="block">
  <h2>Settling Transfers</h2>

  % if len(c.settle) == 0:
    <p>No need! The books are balanced!</p>
  % else:
    <p>To balance the books, the following transfers need to be made:</p>

    <table id="balance">
      <tr>
        <th>From</th>
        <th>To</th>
        <th>Amount</th>
      </tr>
      % for transfer in c.settle:
        <tr>
          <td>${transfer[0].name}</td>
          <td>${transfer[1].name}</td>
          <td class="amount">${transfer[2]}</td>
        </tr>
      % endfor
      % if c.net != 0:
        <tr>
          <th colspan="2">
            % if c.net > 0:
              The group owes you:
            % elif c.net < 0:
              You owe the group:
            % endif
          </th>
          <th class="amount">${abs(c.net)}</th>
        </tr>
      % endif
    </table>
  % endif
</div>

<div class="block">
  <h2>Totals</h2>

  <table id="totals">
    <tr>
      <td class="scope"></td>
      <th class="scope">Everyone</th>
      <th class="scope">My Share</th>
    </tr>
    % for period in ('Total', 'Past year', 'Year to date', 'Month to date', 'Last month'):
      <tr>
        <th>${period}</th>
        % for scope in ('all', 'mine'):
          <td>${c.totals[period][scope]}</td>
        % endfor
      </tr>
    % endfor
  </table>
</div>

<div class="block">
  <h2>
    Your History
    <span class="see-all">
      ${h.link_to('See all history', h.url_for(controller='history', action='index'))}
    </span>
  </h2>

  <h3>Expenditures</h3>

  ${self.listExpenditures(c.expenditures)}

  <h3>Transfers</h3>

  ${self.listTransfers(c.transfers)}
</div>
