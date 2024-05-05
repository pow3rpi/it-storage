export default function Alert(props) {
  const { alert, setAlert } = props;

  const closeAlert = () => {
    setAlert((oldAlert) => ({ ...oldAlert, isVisible: false }));
  };

  return (
    <div id='alert' className='d-flex justify-content-end'>
      <div
        id='liveAlertPlaceholder'
        className={`alert alert-primary pop-up ${
          alert.isFailed ? 'alert-danger' : 'alert-success'
        }`}
        role='alert'
      >
        <div className='d-flex flex-row align-items-center'>
          <div style={{ paddingRight: '5px' }}>
            {alert.isFailed ? 'Failed!' : 'Success!'}
          </div>
          <button
            type='button'
            className='btn-close'
            onClick={closeAlert}
          ></button>
        </div>
      </div>
    </div>
  );
}

let DefaultAlert = {
  isVisible: false,
  isFailed: false,
};

function showAlert(setAlert, isFailed) {
  setAlert({
    isVisible: true,
    isFailed: isFailed,
  });
  setTimeout(
    () => setAlert((oldAlert) => ({ ...oldAlert, isVisible: false })),
    3000
  );
}

export { DefaultAlert, showAlert };
