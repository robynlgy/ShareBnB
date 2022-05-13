/** Presentational Alert component
 *
 * props: alerts(list)
 * state: none
 */
function Alert({ alerts }) {
  return (
    <div className="alert alert-success">
      {alerts.map((alert, idx) => (
        <p key={idx}>{alert}</p>
      ))}
    </div>
  );
}

export default Alert;
