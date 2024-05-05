import ReactMarkdown from 'react-markdown';

import '../css/layout/tutorialPreview.css';

import Tag from '../components/tags/Tag';

export default function TutorialPreview(props) {
  const { title, tags, file, size } = props;

  return (
    <div className='mb-5'>
      <div className='tutorial-preview-title'>Title</div>
      <div className='tutorial-preview-value mb-3'>{title}</div>
      <div className='tutorial-preview-title'>Topics</div>
      <div className='tutorial-preview-value mb-3 col-12 d-flex flex-wrap'>
        {!tags.length ? (
          <div>No topics</div>
        ) : (
          tags.map((tag, index) => (
            <Tag key={index} name={tag} removeOption={false} />
          ))
        )}
      </div>
      <div className='mb-3'>
        <nav>
          <div
            className='nav nav-tabs mb-3 justify-content-between'
            id='nav-tab'
            role='tablist'
          >
            <div className='d-flex flex-row'>
              <button
                className='nav-link active'
                id='nav-preview-tab'
                data-bs-toggle='tab'
                data-bs-target='#nav-preview'
                type='button'
                role='tab'
                aria-controls='nav-preview'
                aria-selected='true'
                style={{ color: 'rgba(101,108,133,0.8)', cursor: 'inherit' }}
              >
                Preview
              </button>
            </div>
            <div className='d-flex align-items-center'>
              <div>{`${(size / 1024).toFixed(1)} KB`}</div>
            </div>
          </div>
        </nav>
        <div className='tab-content' id='nav-tabContent'>
          <div
            className='tab-pane fade show active'
            id='nav-preview'
            role='tabpanel'
            aria-labelledby='nav-preview-tab'
            tabIndex='0'
          >
            {file ? (
              <div className='markdown'>
                <ReactMarkdown children={file} />
              </div>
            ) : (
              <div>No content yet...</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
