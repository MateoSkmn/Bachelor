import { Component, OnDestroy, OnInit } from '@angular/core';
import { HeaderComponent } from '../../global/components/header/header.component';
import { StyledButtonComponent } from '../../global/components/styled-button/styled-button.component';
import { FormsModule } from '@angular/forms';
import { Subject, Subscription, debounceTime } from 'rxjs';
import { ApiService } from '../../global/service/api.service';
import { RecordListItem } from '../../global/interfaces/record-list-item.interface';
import { ErrorService } from '../../global/service/error.service';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { StarEvaluationComponent } from '../../global/components/star-evaluation/star-evaluation.component';
import { MatDialog } from '@angular/material/dialog';
import { LegendeComponent } from './legende/legende.component';
import { MatProgressSpinnerModule} from '@angular/material/progress-spinner'

@Component({
  selector: 'app-lime',
  standalone: true,
  imports: [HeaderComponent, StyledButtonComponent, FormsModule, StarEvaluationComponent, MatProgressSpinnerModule],
  templateUrl: './lime.component.html',
  styleUrl: './lime.component.scss'
})
export class LimeComponent implements OnInit, OnDestroy{

  recordIndex: number = 0;
  maxIndex: number = Number.MAX_SAFE_INTEGER;
  recordName: string = '';
  recordList: RecordListItem[] = [];
  loading: boolean = false;

  formattedText: SafeHtml = '';

  isFilledOut: boolean = false;
  isDisabled: boolean = true;
  understandable: number = 0;
  userPrediction: number = 0;

  actualLabel: number = 0;
  modelPrediction: number = 0;
  limePrediction: number = 0;

  constructor(
    private apiService: ApiService,
    private errorService: ErrorService,
    private sanitizer: DomSanitizer,
    private dialog: MatDialog) {}
  
  private recordListSubscription!: Subscription;
  private limeExplanationSubscription!: Subscription;
  private saveUserInfoSubscription!: Subscription;
  private numberValueChangeSubject = new Subject<number>();

  // Initial Loading of data
  ngOnInit(): void {
    // Loads all records that have a model assigned to them
    this.recordListSubscription = this.apiService.getRecords().subscribe({
      next: (response) => {
        this.recordList = response.filter(item => item.hasModel);
        this.recordName = this.recordList[0].file_name;
        this.requestLimeExplanation();
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });

    // UX extension for index input
    this.numberValueChangeSubject.pipe(
      debounceTime(1000) // Debounce for 1 seconds
    ).subscribe(() => {
      if(this.recordIndex == null) {
        this.recordIndex = 0;
      } else if (this.recordIndex < 0) {
        this.recordIndex *= -1;
      } else if (this.recordIndex > this.maxIndex) {
        this.recordIndex = this.maxIndex;
      }
      this.requestLimeExplanation();
    });
  }

  // Unsubscribe when no longer needed
  ngOnDestroy(): void {
    if (this.recordListSubscription) {
      this.recordListSubscription.unsubscribe();
    }
    if (this.limeExplanationSubscription) {
      this.limeExplanationSubscription.unsubscribe();
    }
    if (this.saveUserInfoSubscription) {
      this.saveUserInfoSubscription.unsubscribe();
    }
  }

  /**
   * Sets the text align so that longer texts are justified and shorter ones are centered. For nicer looking results
   */
  setTextAlign(): void {
    const textContainer = document.getElementById("textContainer");
    if (!textContainer) {
      return;
    }

    // Delay to ensure the layout has been updated
    setTimeout(() => {
      const containerHeight = textContainer.offsetHeight;
      const lineHeight = parseInt(window.getComputedStyle(textContainer).lineHeight);
      const isMultiLine = containerHeight > lineHeight;
      if (isMultiLine) {
        textContainer.style.textAlign = "justify";
      } else {
        textContainer.style.textAlign = "center";
      }
    }, 1);
  }

  /**
   * Request LIME explanation from BE. Also checks if the current instance already has a prediction
   */
  requestLimeExplanation() {
    this.loading = true;
    this.isFilledOut = false;
    this.limeExplanationSubscription = this.apiService.getLime(this.recordName, this.recordIndex).subscribe({
      next: (response) => {
        this.formattedText = this.colorWordsBasedOnValues(response.text, response.lime_values);
        this.loading = false;
        this.setTextAlign();
        this.maxIndex = response.max_index

        if (response.user_predicted_label) {
          this.isFilledOut = true;
          this.actualLabel = response.actual_label;
          this.limePrediction = response.lime_predicted_label;
          this.modelPrediction = response.model_predicted_label;
          this.userPrediction = response.user_predicted_label;
          this.understandable = response.user_understandable;
        }
        else {
          this.isFilledOut = false;
          this.isDisabled = true;
        }
      },
      error: (error) => {
        this.formattedText = "";
        this.errorService.triggerError(error);
      }
    });
  }

  /**
   * Trigger when index value is changed
   */
  onIndexChange() {
    this.numberValueChangeSubject.next(this.recordIndex);
  }

  /**
   * Trigger when selected record is changed
   * @param value Selected record name
   */
  onSelectChange(value: string) {
    this.recordName = value;
    this.requestLimeExplanation();
  }

  /**
   * Request LIME explanation for random value within bounds
   */
  randomIndex() {
    this.recordIndex = Math.floor(Math.random() * (this.maxIndex + 1));
    this.requestLimeExplanation();
  }

  /**
   * Marks the words from the LIME explanation with different colors based on the predicted label.
   * This comes with the drawback that there is no difference between the same word with different meanings!
   * @param text Instance of selected text
   * @param limeValues LIME explanation values
   * @returns Formatted text with colored words as SafeHtml
   */
  colorWordsBasedOnValues(text: string, limeValues: any[]): SafeHtml {
    const colorMap: any = {
      1: 'rgba(255, 0, 0, ALPHA)', // red
      2: 'rgba(255, 165, 0, ALPHA)', // orange
      3: 'rgba(255, 255, 0, ALPHA)', // yellow
      4: 'rgba(0, 255, 0, ALPHA)', // lime
      5: 'rgba(0, 200, 0, ALPHA)' // green
    };

    let coloredText = '';

    //Split by word
    const words = text.split(/\b/);
    words.forEach((word) => {
      //Find words that are in text & limeValues
      const found = limeValues.find((value) => value.word.toLowerCase() === word.toLowerCase());
      if (found) {
        let alpha = found.value;
        const color = colorMap[found.index].replace('ALPHA', alpha.toString());
        coloredText += `<span style="background-color: ${color}">${word}</span>`;
      } else {
        coloredText += word;
      }
    });

    // Sanitize the HTML content before returning
    return this.sanitizer.bypassSecurityTrustHtml(coloredText);
  }

  /**
   * Save user data
   */
  saveEvaluation() {
    const body = [this.recordIndex, this.understandable, this.userPrediction];
    this.saveUserInfoSubscription = this.apiService.postEvaluation(this.recordName, body).subscribe({
      next: () => {
        this.requestLimeExplanation();
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });
  }

  /**
   * Open a dialog window
   */
  openLegende() {
    this.dialog.open(LegendeComponent, {
      width: '500px',
      disableClose: true
    });
  }

  /**
   * Update user data when interacted with the star component
   * @param value Index of the selected star
   * @param isForUnderstandable Check what the component is for
   */
  onFilledStarsChange(value: number, isForUnderstandable: boolean) {
    if (isForUnderstandable) {
      this.understandable = value;
      return;
    }
    this.userPrediction = value;

    if(this.understandable != 0 && this.userPrediction != 0) {
      this.isDisabled = false;
    }
  }
}
