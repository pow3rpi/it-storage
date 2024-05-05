import TagSection from '../components/tags/TagSection';
import { Config } from '../config';

export default function LinkForm(props) {
  const {
    useControlPanel = true,
    btnId = null,
    btnName = null,
    onClick = null,
    tags,
    setTags,
    title,
    url,
    annotation,
  } = props;

  return (
    <form id='link-form' className='pb-5'>
      <div className='mb-3'>
        <label htmlFor='link-title' className='form-label'>
          Title <span className='required-field'>*</span>
        </label>
        <div>
          <input
            id='link-title'
            className='form-control'
            type='text'
            name='title'
            defaultValue={title}
            maxLength={Config.MAX_TITLE_LENGTH}
            required
          />
        </div>
      </div>
      <div className='mb-3'>
        <TagSection
          inputId='link-tags'
          chosenTags={tags}
          setChosenTags={setTags}
        />
      </div>
      <div className='mb-3'>
        <label htmlFor='link-url' className='form-label'>
          URL <span className='required-field'>*</span>
        </label>
        <div>
          <input
            id='link-url'
            className='form-control'
            type='text'
            name='url'
            defaultValue={url}
            required
          />
        </div>
      </div>
      <div className='mb-3'>
        <label htmlFor='link-annotation' className='form-label'>
          Annotation
        </label>
        <div>
          <textarea
            id='link-annotation'
            className='form-control'
            type='text'
            name='annotation'
            defaultValue={annotation}
            maxLength={Config.MAX_ANNOTATION_LENGTH}
          />
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
