import $ from 'jquery';

import '../../css/components/controlPanel.css';

import { SearchType, SearchBy } from '../../js/enum/search';
import { activateOption, deactivateOption } from '../../js/style/searchOptions';

export default function ControlPanel(props) {
  const { searchFilter, setSearchFilter } = props;
  const searchByName = $('#search-name');
  const searchByTopic = $('#search-topic');
  const typeAll = $('#type-all');
  const typeLink = $('#type-link');
  const typeTutorial = $('#type-tutorial');

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

  const switchToAll = () => {
    setSearchFilter((state) => ({ ...state, type: SearchType.all }));
    deactivateOption(typeLink, typeTutorial);
    activateOption(typeAll);
  };

  const switchToLinkOnly = () => {
    setSearchFilter((state) => ({ ...state, type: SearchType.link }));
    deactivateOption(typeAll, typeTutorial);
    activateOption(typeLink);
  };

  const switchToTutorialOnly = () => {
    setSearchFilter((state) => ({ ...state, type: SearchType.tutorial }));
    deactivateOption(typeAll, typeLink);
    activateOption(typeTutorial);
  };

  return (
    <>
      <div className='d-flex justify-content-end mb-1'>
        <div className='d-flex align-items-center'>
          <div className='d-flex flex-row align-items-center'>
            <div className='d-flex flex-row align-items-center me-2'>
              <div
                id='type-all'
                className='btn-search-filter'
                onClick={switchToAll}
                style={
                  searchFilter.type === SearchType.all
                    ? {
                        backgroundColor: 'var(--color2)',
                        borderColor: 'var(--color1)',
                      }
                    : {}
                }
              >
                {SearchType.all}
              </div>
              <div className='me-1 ms-1'>|</div>
              <div
                id='type-link'
                className='btn-search-filter'
                onClick={switchToLinkOnly}
                style={
                  searchFilter.type === SearchType.link
                    ? {
                        backgroundColor: 'var(--color2)',
                        borderColor: 'var(--color1)',
                      }
                    : {}
                }
              >
                {SearchType.link}
              </div>
              <div className='me-1 ms-1'>|</div>
              <div
                id='type-tutorial'
                className='btn-search-filter'
                onClick={switchToTutorialOnly}
                style={
                  searchFilter.type === SearchType.tutorial
                    ? {
                        backgroundColor: 'var(--color2)',
                        borderColor: 'var(--color1)',
                      }
                    : {}
                }
              >
                {SearchType.tutorial}
              </div>
            </div>
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
                      backgroundColor: 'var(--color2)',
                      borderColor: 'var(--color1)',
                    }
                  : {}
              }
            >
              name
            </div>
            <div className='me-1 ms-1'>|</div>
            <div
              id='search-topic'
              className='btn-search-filter'
              onClick={switchToTopic}
              style={
                searchFilter.searchBy === SearchBy.topic
                  ? {
                      backgroundColor: 'var(--color2)',
                      borderColor: 'var(--color1)',
                    }
                  : {}
              }
            >
              topic
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
