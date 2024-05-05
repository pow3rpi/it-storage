import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import $ from 'jquery';

import '../../css/components/controlPanel.css';

import ModalAlert from '../ModalAlert';
import { SearchBy } from '../../js/enum/search';
import { activateOption, deactivateOption } from '../../js/style/searchOptions';

export default function ControlPanel(props) {
  const {
    onDelete,
    cancelDelete,
    searchFilter,
    setSearchFilter,
    isDeleteMode,
    setIsDeleteMode,
  } = props;
  const navigate = useNavigate();
  const [btnName, setBtnName] = useState(
    window.screen.width >= 600 ? 'Create' : ''
  );
  const searchByName = $('#search-name');
  const searchByTopic = $('#search-topic');
  const modalId = 'modalAlert';

  window.onresize = () => {
    setBtnName(window.screen.width >= 600 ? 'Create' : '');
  };

  document.onkeydown = function (event) {
    if (event.key === 'Escape') {
      document.onkeydown = null;
      cancelDelete();
    }
  };

  const switchToTopic = () => {
    setSearchFilter((state) => ({ ...state, searchBy: SearchBy.topic }));
    deactivateOption(searchByName);
    activateOption(searchByTopic);
  };

  const switchToName = () => {
    setSearchFilter((state) => ({ ...state, searchBy: SearchBy.name }));
    deactivateOption(searchByTopic);
    activateOption(searchByName);
  };

  return (
    <>
      <ModalAlert
        id={modalId}
        text='Do you want to permanently delete all chosen posts?'
        onClick={onDelete}
        btnActionName='Delete'
      />
      <div
        className='d-flex justify-content-between content-control-panel mb-3'
        style={{ paddingBottom: '2px' }}
      >
        <div
          className='btn-back d-flex align-items-center'
          onClick={() => navigate('/manage_content')}
        >
          <div>
            <i className='icon-arrow-left'></i>Back
          </div>
        </div>
        <div className='d-flex align-items-center'>
          <div className='d-flex flex-row align-items-center me-2'>
            <div className='me-2' style={{ color: 'rgba(0, 0, 0, 0.55)' }}>
              Search by:
            </div>
            <div
              id='search-name'
              className='btn-search-filter'
              onClick={switchToName}
              style={
                searchFilter.searchBy === SearchBy.name
                  ? {
                      backgroundColor: 'var(--color3)',
                      borderColor: 'var(--color1)',
                    }
                  : {}
              }
            >
              {SearchBy.name}
            </div>
            <div className='me-1 ms-1'>|</div>
            <div
              id='search-topic'
              className='btn-search-filter'
              onClick={switchToTopic}
              style={
                searchFilter.searchBy === SearchBy.topic
                  ? {
                      backgroundColor: 'var(--color3)',
                      borderColor: 'var(--color1)',
                    }
                  : {}
              }
            >
              {SearchBy.topic}
            </div>
          </div>
          <div className='me-2 btn-create' onClick={() => navigate(`create`)}>
            <i className='icon-plus'></i>
            {btnName}
          </div>
          {isDeleteMode ? (
            <div className='d-flex flex-row align-items-center'>
              <i
                className='icon-accept icon-search-panel'
                data-bs-toggle='modal'
                data-bs-target={'#' + modalId}
              ></i>
              <i
                className='icon-cancel icon-search-panel'
                onClick={cancelDelete}
              ></i>
            </div>
          ) : (
            <i
              className='d-block icon-trash'
              style={{
                fontSize: '19px',
                lineHeight: '19px',
              }}
              onClick={() => setIsDeleteMode(true)}
            ></i>
          )}
        </div>
      </div>
    </>
  );
}
