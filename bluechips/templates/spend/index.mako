<%inherit file="/base.mako"/>

<%!
    from decimal import Decimal
%>

<form action="${h.url_for(controller='spend', action='update', id=c.expenditure.id)}" method="post">
  <table class="form">
    <tr>
      <th><label for="spender_id">Spender</label></th>
      <td>${h.select('spender_id', c.expenditure.spender_id, c.users)}</td>
    </tr>
    <tr>
      <th><label for="amount">Amount</label></th>
      <td>$${h.text('amount', "%0.2f" % (int(c.expenditure.amount) / 100.), size=8)}</td>
    </tr>
    <tr>
      <th><label for="date">Date</label></th>
      <td>${h.text('date', c.expenditure.date.strftime('%m/%d/%Y'), size=16, class_='datepicker')}</td>
    </tr>
    <tr>
      <th><label for="description">Description</label></th>
      <td>${h.text('description', c.expenditure.description, size=64)}</td>
    </tr>
  </table>

  <p>Change how an expenditure is split up. Enter a percentage, or something like a percentage, for each user. They don't have to add to 100.</p>

  <table class="form">
    % for user_id, user in c.users:
      <%
        try:
            percent = c.values['shares-%d.amount' % user_id]
        except TypeError:
            if c.id != '':
                try:
                    share = [s.share for s in c.expenditure.splits if s.user == user][0]
                    percent = (Decimal(100) * Decimal(int(share)) / Decimal(int(c.expenditure.amount))).quantize(Decimal("0.001"))
                except IndexError:
                    percent = 0
            else:
                if user == request.environ['user']:
                    percent = 1
                else:
                    percent = 0
      %>
      <tr>
        <th>
          <label for="shares-${user_id}amount">${user.name}</label>
        </th>
        <td>
          ${h.text('shares-%d.amount' % user_id, percent)}
          ${h.hidden('shares-%d.user_id' % user_id, user.id)}
        </td>
      </tr>
    % endfor
    <tr>
      <td colspan="2">
        ${h.submit(None, 'Submit', class_="submitbutton")}
      </td>
    </tr>
  </table>
</form>
