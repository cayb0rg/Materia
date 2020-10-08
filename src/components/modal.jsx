import React from 'react'
import { createPortal } from 'react-dom';
import './modal.scss'
import useClickOutside from '../util/use-click-outside'




// We get hold of the div with the id modal that we have created in index.html
const modalRoot = document.getElementById( 'modal' );

class Modal extends React.Component {
	constructor( props ) {
		super( props );
		// create an element div for this modal
		this.modalRef = React.createRef();
		this.element = document.createElement( 'div' );
		this.clickOutsideListener = this.clickOutsideListener.bind(this)
	}

	clickOutsideListener(event){
		// Do nothing if clicking ref's element or descendent elements
		if (!this.modalRef.current || this.modalRef.current.contains(event.target)) {
			return;
		}

		this.props.onClose()
	};

	componentDidMount() {
		modalRoot.appendChild( this.element );
		document.addEventListener('mousedown', this.clickOutsideListener);
  		document.addEventListener('touchstart', this.clickOutsideListener);
	}

	componentWillUnmount() {
		modalRoot.removeChild( this.element );
		document.removeEventListener('mousedown', this.clickOutsideListener);
		document.removeEventListener('touchstart', this.clickOutsideListener);
	}

	render() {
	  const stuff = (
		<>
			<div className="modal-overlay" id="modal-overlay"></div>

			<div ref={this.modalRef} className="modal" id="modal">
				<button className="close-button" id="close-button" onClick={this.props.onClose}>X</button>
				<div className="modal-guts">
					{this.props.children}
				</div>
			</div>
		</>
	  )
	  return createPortal( stuff, this.element );
   }
}

export default Modal