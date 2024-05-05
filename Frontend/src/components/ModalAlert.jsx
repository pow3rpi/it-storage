export default function ModalAlert(props) {
  const { id, text, onClick, btnActionName } = props;

  return (
    <div
      className='modal fade'
      id={id}
      data-bs-backdrop='static'
      data-bs-keyboard='false'
      tabIndex='-1'
      aria-labelledby={id + 'Label'}
      aria-hidden='true'
    >
      <div className='modal-dialog modal-dialog-centered'>
        <div className='modal-content'>
          <div className='modal-header'>
            <h1 className='modal-title fs-5' id={id + 'Label'}>
              Confirm action
            </h1>
            <button
              type='button'
              className='btn-close me-1'
              data-bs-dismiss='modal'
              aria-label='Close'
            ></button>
          </div>
          <div className='modal-body'>{text}</div>
          <div className='modal-footer'>
            <button
              type='button'
              className='btn btn-danger'
              onClick={onClick}
              data-bs-dismiss='modal'
            >
              {btnActionName}
            </button>
            <button
              type='button'
              className='btn btn-secondary'
              data-bs-dismiss='modal'
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
