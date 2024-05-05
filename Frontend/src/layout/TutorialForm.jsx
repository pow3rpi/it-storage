import ReactMarkdown from 'react-markdown';

import TagSection from '../components/tags/TagSection';
import { Config } from '../config.js';

export default function TutorialForm(props) {
  const {
    useControlPanel = true,
    btnId = null,
    btnName = null,
    onClick = null,
    tags,
    setTags,
    tutorial,
    setTutorial,
  } = props;

  return (
    <form id='tutorial-form' className='mb-5'>
      <div className='mb-3 col-12 col-xl-5 col-lg-6'>
        <label htmlFor='tutorial-title' className='form-label'>
          Title <span className='required-field'>*</span>
        </label>
        <div>
          <input
            id='tutorial-title'
            className='form-control'
            type='text'
            name='title'
            defaultValue={tutorial.title}
            maxLength={Config.MAX_TITLE_LENGTH}
            required
          />
        </div>
      </div>
      <div className='mb-3 col-12 col-xl-5 col-lg-6'>
        <TagSection
          inputId='link-tags'
          chosenTags={tags}
          setChosenTags={setTags}
        />
      </div>
      <div className='mb-3'>
        <nav>
          <div
            id='nav-tab'
            className='nav nav-tabs mb-3 justify-content-between'
            role='tablist'
          >
            <div className='d-flex flex-row'>
              <button
                id='nav-markdown-tab'
                className='nav-link active'
                data-bs-toggle='tab'
                data-bs-target='#nav-markdown'
                type='button'
                role='tab'
                aria-controls='nav-markdown'
                aria-selected='true'
              >
                Markdown
              </button>
              <button
                id='nav-preview-tab'
                className='nav-link'
                data-bs-toggle='tab'
                data-bs-target='#nav-preview'
                type='button'
                role='tab'
                aria-controls='nav-preview'
                aria-selected='false'
              >
                Preview
              </button>
            </div>
            <div className='d-flex align-items-center'>
              <div
                style={{
                  color:
                    tutorial.size > Config.MAX_TUTORIAL_SIZE ? 'red' : 'green',
                }}
              >{`${(tutorial.size / 1024).toFixed(1)} KB`}</div>
            </div>
          </div>
        </nav>
        <div className='tab-content' id='nav-tabContent'>
          <div
            id='nav-markdown'
            className='tab-pane fade show active'
            role='tabpanel'
            aria-labelledby='nav-markdown-tab'
            tabIndex='0'
          >
            <textarea
              id='tutorial-file'
              className='form-control'
              name='file'
              value={tutorial.file}
              onChange={(event) =>
                setTutorial({
                  ...tutorial,
                  file: event.target.value,
                  size: new Blob([event.target.value]).size,
                })
              }
              required
            />
          </div>
          <div
            id='nav-preview'
            className='tab-pane fade'
            role='tabpanel'
            aria-labelledby='nav-preview-tab'
            tabIndex='0'
          >
            {tutorial.file ? (
              <div className='markdown'>
                <ReactMarkdown children={tutorial.file} />
              </div>
            ) : (
              <div>No content yet...</div>
            )}
          </div>
        </div>
      </div>
      <div
        id='error-alert'
        className='d-none alert alert-danger mb-3'
        role='alert'
      ></div>
      {useControlPanel ? null : (
        <button
          id={btnId}
          className='btn btn-primary btn-standard float-end mb-5'
          type='button'
          onClick={onClick}
        >
          {btnName}
        </button>
      )}
    </form>
  );
}
