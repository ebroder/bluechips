<%inherit file="/base.mako"/>

<h2>Settling Transfers</h2>

% if len(c.settle) == 0:
<p>No need! The books are balanced!</p>
% else:
<p>To balance the books, the following transfers need to be made:</p>

<table>
    <tr>
        <th>From</th>
        <th>To</th>
        <th>Amount</th>
    </tr>
    % for transfer in c.settle:
    <tr>
        <td>${transfer[0].username}</td>
        <td>${transfer[1].username}</td>
        <td>$${h.round_currency(transfer[2])}</td>
    </tr>
    % endfor
</table>
% endif

<h2>Totals</h2>

<table>
    <tr>
        <td>Total</td>
        <td>$${h.round_currency(c.total)}</td>
    </tr>
    <tr>
        <td>Past year</td>
        <td>$${h.round_currency(c.year_total)}</td>
    </tr>
    <tr>
        <td>Year to date</td>
        <td>$${h.round_currency(c.this_year_total)}</td>
    </tr>
    <tr>
        <td>Month to date</td>
        <td>$${h.round_currency(c.this_month_total)}</td>
    </tr>
    <tr>
        <td>Last month</td>
        <td>$${h.round_currency(c.last_month_total)}</td>
    </tr>
</table>

<h2>Add a new transaction</h2>

<ul>
    <li>${h.link_to('Expenditure for the group', h.url_for(controller='spend', action='index'))}</li>
    <li>${h.link_to('Transfer between two people', h.url_for(controller='transfer', action='index'))}</li>
</ul>

<h2>Your History</h2>

${h.link_to('See all history', h.url_for(controller='history',
                                         action='index'))}

<h3>Expenditures</h3>

${self.listExpenditures(c.expenditures)}

<h3>Transfers</h3>

${self.listTransfers(c.transfers)}
