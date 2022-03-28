import React, { Component } from 'react';
import { defaultProps, propTypes } from '../components/SearchBar.react';
import "./style.css";

export default class SearchBar extends Component {


    constructor(props) {
        super(props);

        this.state = {
            active: (props.locked && props.active) || false,
            value: props.value || "",
            label: props.label || "Label",
            searchTerm: props.searchTerm || "",
            submitted: Boolean
        };
    }

    //Sets state.value whenever the user types in the searchbar.
    changeValue(event) {
        const value = event.target.value;
        this.setState({ value });
    }

    //Sets props.value whenever the user clicks the search button.
    handleClick(event) {
        this.props.setProps({ value: this.state.value });
    }


    render() {
        const { active, value, label } = this.state;
        const { predicted, locked } = this.props;
        const fieldClassName = `field ${(locked ? active : active || value) &&
            "active"} ${locked && !active && "locked"}`;

        return (
            <span>
               
                <div className={fieldClassName}>
                    {active &&
                        value &&
                        predicted &&
                        predicted.includes(value) && <p className="predicted">{predicted}</p>}

                    <input
                        id={1}
                        type="text"
                        value={value}
                        placeholder={label}
                        onChange={this.changeValue.bind(this)}
                        onFocus={() => !locked && this.setState({ active: true })}
                        onBlur={() => !locked && this.setState({ active: false })}
                    />
                </div>
                <button onClick={this.handleClick.bind(this)} className="clickSearchButton">
                    Search
                </button>
            </span>
        );
    }
}


SearchBar.defaultProps = defaultProps;
SearchBar.propTypes = propTypes;