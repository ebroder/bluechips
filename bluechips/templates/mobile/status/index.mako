<%inherit file="/mobile/base.mako"/>

${self.tabs('status')}

<div id="tab-status" class="tab">
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
${self.spendForm()}
${self.transferForm()}
