import React, { useState } from 'react';
import $ from 'jquery';

import '../../css/components/tag.css';
import '../../css/components/search.css';

import Tag from './Tag';
import TagList from './TagList';
import getTags from '../../js/api/getTags';
import logOutRequest from '../../js/api/logOut';
import { normalizeTag } from '../../js/processing/normalizer';
import { Config } from '../../config';
import { defaultTags } from '../../data/defaultTags';

export default function TagSection(props) {
  const {
    inputId,
    chosenTags,
    setChosenTags,
    searchMode = false,
    onSearch = null,
  } = props;
  const [suggestedTags, setSuggestedTags] = useState(defaultTags);
  const [value, setValue] = useState('');
  const [isFound, setIsFound] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const tagListId = 'tags-list';

  const addTag = (tag) => {
    if (chosenTags.length < Config.MAX_N_TAGS) {
      const newTag = normalizeTag(tag);
      if (!chosenTags.includes(newTag) && newTag !== '') {
        setChosenTags((oldTags) => [...oldTags, newTag]);
      }
    }
  };

  const handleKey = (event) => {
    if (event.key === 'Enter') {
      if (searchMode && event.target.value === '') {
        onSearch();
        $(`#${tagListId}`).addClass('d-none');
        return;
      }
      addTag(event.target.value);
      event.target.value = '';
      setValue('');
      $(`#${tagListId}`).addClass('d-none');
      document.getElementById(inputId).blur();
      setSuggestedTags(defaultTags);
    }
  };

  const getSimilarTags = async (event) => {
    const curValue = event.target.value;
    let doRequest = true;
    if (curValue.length > 3 && !isFound && curValue.length > value.length) {
      doRequest = false;
    }
    setValue(curValue);
    setIsFound(false);
    switch (true) {
      case curValue.length === 0:
        setSuggestedTags(defaultTags);
        break;
      case curValue.length > 0 && curValue.length <= 2:
        setSuggestedTags([curValue]);
        break;
      default:
        if (doRequest) {
          setIsSearching(true);
          await getTags(curValue).then((data) => {
            if (data.detail !== undefined) {
              logOutRequest();
            } else {
              setIsSearching(false);
              if (data.tags.length > 0) {
                setSuggestedTags(data.tags);
                setIsFound(true);
              } else {
                setSuggestedTags([curValue]);
              }
            }
          });
        } else {
          setSuggestedTags([curValue]);
        }
        break;
    }
  };

  return (
    <>
      {searchMode ? null : (
        <label htmlFor={inputId} className='form-label'>
          Topics
        </label>
      )}
      <div className='input-group'>
        <input
          id={inputId}
          className={`form-control ${searchMode ? 'search-line' : ''}`}
          type='text'
          name='tags'
          placeholder={`Search ${searchMode ? 'by' : 'for'} topic`}
          aria-describedby='search-btn'
          maxLength={Config.MAX_TAG_LENGTH}
          onKeyDown={handleKey}
          onChange={getSimilarTags}
          onFocus={() => $(`#${tagListId}`).removeClass('d-none')}
          onBlur={() => $(`#${tagListId}`).addClass('d-none')}
        />
        {searchMode ? (
          <span
            id='search-btn'
            className='input-group-text btn-search'
            onClick={onSearch}
          >
            <i className='icon-search'></i>
          </span>
        ) : null}
      </div>
      <div>
        <TagList
          tagListId={tagListId}
          suggestedTags={suggestedTags}
          setSuggestedTags={setSuggestedTags}
          addTag={addTag}
          inputId={inputId}
          value={value}
          setValue={setValue}
          isFound={isFound}
          isSearching={isSearching}
        />
        <div className='col-12 d-flex flex-wrap'>
          {!chosenTags.length
            ? null
            : chosenTags.map((tag, index) => (
                <Tag key={index} name={tag} setTags={setChosenTags} />
              ))}
        </div>
      </div>
    </>
  );
}
