import { useNavigate } from 'react-router-dom';

import '../../css/components/controlPanel.css';

import ModalAlert from '../ModalAlert';
import deletePostsRequest from '../../js/api/deletePosts';
import logOutRequest from '../../js/api/logOut';
import { showAlert } from '../Alert';

export default function ControlPanel(props) {
  const {
    id,
    setAlert,
    isEdit,
    onEdit,
    onCancel,
    onAccept,
    isWaitingResponse,
  } = props;
  const navigate = useNavigate();
  const modalId = 'modalAlert';

  document.onkeydown = function (event) {
    if (event.key === 'Escape') {
      document.onkeydown = null;
      onCancel();
    }
  };

  const deletePost = async () => {
    const requestBody = JSON.stringify({ id: [id] });
    await deletePostsRequest(requestBody).then((data) => {
      const error_code = data.error_code;
      if (error_code !== undefined) {
        error_code === 12 ? logOutRequest() : showAlert(setAlert, true);
      } else {
        navigate(-1);
      }
    });
  };

  return (
    <>
      <ModalAlert
        id={modalId}
        text='Do you want to permanently delete this post?'
        onClick={deletePost}
        btnActionName='Delete'
      />
      <div
        className='d-flex justify-content-between align-items-center content-control-panel mb-3'
        style={{ opacity: isWaitingResponse ? 0.6 : 1 }}
      >
        <div
          className='btn-back'
          onClick={isWaitingResponse ? null : () => navigate(-1)}
        >
          <i className='icon-arrow-left'></i>Back
        </div>
        <div className='d-flex align-items-center'>
          {isEdit ? (
            <>
              <i
                className='d-block icon-accept icon-content-panel'
                onClick={isWaitingResponse ? null : onAccept}
              ></i>
              <i
                className='d-block icon-cancel icon-content-panel'
                onClick={isWaitingResponse ? null : onCancel}
              ></i>
            </>
          ) : (
            <i
              className='d-block icon-edit icon-content-panel'
              onClick={isWaitingResponse ? null : onEdit}
            ></i>
          )}
          <i
            className='d-block icon-trash'
            style={{
              fontSize: '21px',
              lineHeight: '21px',
              paddingBottom: '2px',
            }}
            data-bs-toggle={isWaitingResponse ? '' : 'modal'}
            data-bs-target={`#${modalId}`}
          ></i>
        </div>
      </div>
    </>
  );
}
